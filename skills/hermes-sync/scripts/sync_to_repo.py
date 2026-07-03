import os
import shutil
import yaml
import re
import subprocess
import json
from datetime import datetime

# CONFIGURATION
HERMES_HOME = os.path.expanduser("~/.hermes")
REPO_ROOT = os.path.expanduser("~/hermes-sync-dev/repo_template")
# In a real deployment, this would be the path to the actual git repo
# For now, we use the dev directory.
LOCAL_REPO_PATH = os.path.expanduser("~/hermes-sync-dev/repo_template")

REDACT_PATTERNS = [
    r"(?i)api_key\s*[:=]\s*['\"]?([^'\"]+)['\"]?",
    r"(?i)token\s*[:=]\s*['\"]?([^'\"]+)['\"]?",
    r"(?i)secret\s*[:=]\s*['\"]?([^'\"]+)['\"]?",
    r"(?i)password\s*[:=]\s*['\"]?([^'\"]+)['\"]?",
]

def redact_text(text):
    for pattern in REDACT_PATTERNS:
        text = re.sub(pattern, r"\1='[REDACTED]'", text)
    return text

def sync_config():
    print("--- Syncing Config ---")
    config_path = os.path.join(HERMES_HOME, "config.yaml")
    dest_path = os.path.join(REPO_ROOT, "configs/config.yaml")
    
    if not os.path.exists(config_path):
        print(f"Warning: Config not found at {config_path}")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    def redact_dict(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if any(secret_word in k.lower() for secret_word in ["key", "token", "secret", "password"]):
                    d[k] = "[REDACTED]"
                else:
                    redact_dict(v)
        elif isinstance(d, list):
            for item in d:
                redact_dict(item)

    redact_dict(config)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"Saved redacted config to {dest_path}")

def sync_skills():
    print("--- Syncing Skills ---")
    skills_dir = os.path.join(HERMES_HOME, "skills")
    dest_skills_dir = os.path.join(REPO_ROOT, "skills")
    
    if not os.path.exists(skills_dir):
        print(f"Warning: Skills dir not found at {skills_dir}")
        return

    if os.path.exists(dest_skills_dir):
        shutil.rmtree(dest_skills_dir)
    
    shutil.copytree(skills_dir, dest_skills_dir)
    print(f"Copied skills to {dest_skills_dir}")

def sync_cron():
    print("--- Syncing Cron Manifest ---")
    # To actually get cron jobs, we'd ideally use `hermes cron list`
    # Since we are in a script, we can try running it via subprocess
    dest_path = os.path.join(REPO_ROOT, "cron/manifest.json")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    manifest = []
    try:
        # Attempt to get cron jobs via CLI
        result = subprocess.run(["hermes", "cron", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            # This is a simplified parser. In a real implementation, 
            # we'd parse the actual CLI output format.
            print("Detected cron jobs via CLI.")
            # manifest = parse_hermes_cron_output(result.stdout)
        else:
            print("Could not retrieve cron jobs via CLI (perhaps no jobs or CLI error).")
    except Exception as e:
        print(f"Error running hermes cron list: {e}")

    with open(dest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written to {dest_path}")

def main():
    os.makedirs(REPO_ROOT, exist_ok=True)
    sync_config()
    sync_skills()
    sync_cron()
    print("\n--- Sync Complete! ---")
    print(f"Your repo is ready at: {REPO_ROOT}")

if __name__ == "__main__":
    main()
