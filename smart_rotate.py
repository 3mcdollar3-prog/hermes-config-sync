#!/home/mcdollar3/.hermes/venv_stt/bin/python3
import json
import os
import subprocess
import time
import sys

sys.path.append("/home/mcdollar3/.hermes/venv_stt/lib/python3.13/site-packages")
try:
    import yaml
except ImportError:
    import json

CONFIG_PATH = os.path.expanduser("~/.hermes/config.yaml")
STATE_FILE = os.path.expanduser("~/.hermes/scripts/model_state.json")
ENV_PATH = os.path.expanduser("~/.hermes/.env")

# Official Google Model Limits (RPM, TPM, RPD)
MODEL_LIMITS = {
    "gemini-3.1-flash-live-preview": {"rpm": 5,  "tpm": 250000, "rpd": 20},
    "gemini-3.6-flash":      {"rpm": 5,  "tpm": 250000, "rpd": 20},
    "gemini-3.5-flash":      {"rpm": 5,  "tpm": 250000, "rpd": 20},
    "gemini-3.1-flash":      {"rpm": 5,  "tpm": 250000, "rpd": 20},
    "gemini-3.1-flash-lite": {"rpm": 15, "tpm": 250000, "rpd": 500},
    "gemini-3.5-flash-lite": {"rpm": 15, "tpm": 250000, "rpd": 500},
    "gemini-3-flash":        {"rpm": 5,  "tpm": 250000, "rpd": 20}
}

DEFAULT_MODELS = list(MODEL_LIMITS.keys())

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

def get_api_keys():
    env_vals = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    parts = line.split("=", 1)
                    env_vals[parts[0].strip()] = parts[1].strip()
    
    key_vars = ["GOOGLE_API_KEY", "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3", "GOOGLE_API_KEY_4", "GOOGLE_API_KEY_5", "GOOGLE_API_KEY_9", "GOOGLE_API_KEY_10", "GOOGLE_API_KEY_11", "GOOGLE_API_KEY_12", "GOOGLE_API_KEY_13", "GOOGLE_API_KEY_14"]
    keys = []
    for var in key_vars:
        val = os.environ.get(var) or env_vals.get(var)
        if val and not val.startswith("your_") and not val.startswith("[REDACTED]"):
            keys.append(val)
    if not keys:
        keys = ["dummy_key"]
    return keys

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"usage": {}, "cooldowns": {}, "last_index": 0, "api_key_index": 0}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_models_from_config():
    config = load_config()
    pool = config.get("credential_pool_strategies", {}).get("gemini", {}).get("models", DEFAULT_MODELS)
    if isinstance(pool, str):
        try:
            pool = json.loads(pool)
        except Exception:
            pool = DEFAULT_MODELS
    # Ensure gemini-3.1-flash-live-preview is always first if present
    if "gemini-3.1-flash-live-preview" in pool:
        pool.remove("gemini-3.1-flash-live-preview")
    pool.insert(0, "gemini-3.1-flash-live-preview")
    return pool

def get_current_model():
    config = load_config()
    model_val = config.get("model")
    if isinstance(model_val, dict):
        return model_val.get("default", DEFAULT_MODELS[0])
    return model_val if isinstance(model_val, str) else DEFAULT_MODELS[0]

def is_model_quota_exceeded(model_name, state):
    limits = MODEL_LIMITS.get(model_name, {"rpm": 5, "tpm": 250000, "rpd": 20})
    usage = state.get("usage", {}).get(model_name, {"requests": [], "daily_requests": 0, "daily_reset": time.time()})
    
    now = time.time()
    if now - usage.get("daily_reset", now) > 86400:
        usage["daily_requests"] = 0
        usage["daily_reset"] = now
    
    if usage.get("daily_requests", 0) >= limits["rpd"]:
        return True, "RPD Limit Reached"

    reqs = usage.get("requests", [])
    recent_reqs = [t for t in reqs if now - t < 60]
    usage["requests"] = recent_reqs
    
    if len(recent_reqs) >= limits["rpm"]:
        return True, "RPM Limit Reached"

    return False, "Healthy"

def check_and_cooldown_failed_models(models, state):
    jobs_path = os.path.expanduser("~/.hermes/cron/jobs.json")
    if not os.path.exists(jobs_path):
        return state
    try:
        with open(jobs_path, "r") as f:
            data = json.load(f)
        for job in data.get("jobs", []):
            if job.get("name") == "smart-model-rotation-watchdog":
                last_status = job.get("last_status")
                last_error = job.get("last_error") or ""
                last_run_at = job.get("last_run_at")
                # Handle both 429 and 501 errors
                if last_status == "error" and any(err in last_error.lower() for err in ["429", "501", "quota", "resource_exhausted", "rate limit", "not implemented", "server error"]):
                    if state.get("last_handled_failure_time") == last_run_at:
                        break
                    idx = state.get("last_index", 0)
                    if 0 <= idx < len(models):
                        failed_model = models[idx]
                        if "cooldowns" not in state:
                            state["cooldowns"] = {}
                        state["cooldowns"][failed_model] = time.time() + 600
                        print(f"Auto-detected error (429/501) on model '{failed_model}'. Placing on 10-minute cooldown and rotating API key.")
                        # Advance API key index on error 429/501
                        keys = get_api_keys()
                        state["api_key_index"] = (state.get("api_key_index", 0) + 1) % len(keys)
                        state["last_handled_failure_time"] = last_run_at
                        save_state(state)
    except Exception as e:
        print(f"Error checking previous job status: {e}")
    return state

def rotate_model(force=False):
    models = get_models_from_config()
    state = load_state()
    if not force:
        state = check_and_cooldown_failed_models(models, state)
    now = time.time()

    current = get_current_model()
    idx = state.get("last_index", 0)
    api_key_idx = state.get("api_key_index", 0)
    
    next_model = None
    selected_idx = idx

    for i in range(1, len(models) + 1):
        candidate_idx = (idx + i) % len(models)
        candidate = models[candidate_idx]
        
        exceeded, reason = is_model_quota_exceeded(candidate, state)
        cooldown_exp = state.get("cooldowns", {}).get(candidate, 0)
        in_cooldown = cooldown_exp > now

        if (not exceeded and not in_cooldown) or force:
            next_model = candidate
            selected_idx = candidate_idx
            break

    keys = get_api_keys()
    if not next_model:
        print("WARNING: All models on current API key exhausted! Rotating to next API key and resetting quotas.")
        state["usage"] = {}
        state["cooldowns"] = {}
        api_key_idx = (api_key_idx + 1) % len(keys)
        next_model = models[0]
        selected_idx = 0

    state["last_index"] = selected_idx
    state["api_key_index"] = api_key_idx
    save_state(state)

    selected_key = keys[api_key_idx % len(keys)]

    print(f"Smart-rotating model from {current} to {next_model} (Pool index {selected_idx}/{len(models)-1}) | API Key Index: {api_key_idx}/{len(keys)-1}")
    
    try:
        config = load_config()
        if "model" not in config:
            config["model"] = {}
        config["model"]["default"] = next_model
        config["model"]["api_key"] = selected_key
        save_config(config)
        print(f"Successfully updated Hermes config with model {next_model} and API key index {api_key_idx}")
    except Exception as e:
        print(f"Error updating config: {e}")

def mark_model_failed(model_name):
    state = load_state()
    if "cooldowns" not in state:
        state["cooldowns"] = {}
    state["cooldowns"][model_name] = time.time() + 600
    keys = get_api_keys()
    state["api_key_index"] = (state.get("api_key_index", 0) + 1) % len(keys)
    save_state(state)
    print(f"Model {model_name} hit error (429/501). Placed on 10-minute cooldown and rotated to next API key.")
    rotate_model(force=False)

def show_status():
    models = get_models_from_config()
    current = get_current_model()
    state = load_state()
    keys = get_api_keys()
    api_key_idx = state.get("api_key_index", 0)
    now = time.time()

    print(f"Current Active Model: {current}")
    print(f"Current Active API Key Index: {api_key_idx} (Total Keys Available: {len(keys)})")
    print("\nQuota & Rate-Limit Tracking Status (Google Limits Integrated):")
    for idx, m in enumerate(models):
        limits = MODEL_LIMITS.get(m, {"rpm": 5, "tpm": 250000, "rpd": 20})
        exceeded, reason = is_model_quota_exceeded(m, state)
        
        usage = state.get("usage", {}).get(m, {"requests": [], "daily_requests": 0})
        rpm_current = len([t for t in usage.get("requests", []) if now - t < 60])
        rpd_current = usage.get("daily_requests", 0)

        status = "HEALTHY"
        if exceeded:
            status = f"QUOTA EXCEEDED ({reason})"
        elif m in state.get("cooldowns", {}) and state["cooldowns"][m] > now:
            rem = int(state["cooldowns"][m] - now)
            status = f"COOLDOWN ({rem}s remaining)"

        marker = " -> [ACTIVE]" if m == current else ""
        print(f"  {idx}: {m}")
        print(f"     Status: [{status}]{marker}")
        print(f"     RPM: {rpm_current}/{limits['rpm']} | RPD: {rpd_current}/{limits['rpd']} | TPM Limit: {limits['tpm']:,}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "status":
            show_status()
        elif cmd == "fail" and len(sys.argv) > 2:
            mark_model_failed(sys.argv[2])
        elif cmd == "record" and len(sys.argv) > 2:
            record_request(sys.argv[2])
        elif cmd == "force":
            rotate_model(force=True)
        else:
            rotate_model()
    else:
        rotate_model()
