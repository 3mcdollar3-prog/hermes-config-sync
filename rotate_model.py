
import json
import os
import subprocess
import time

STATE_FILE = os.path.expanduser("~/.hermes/scripts/model_state.json")

# Define the model rotation sequence with weights
# Weights represent relative capacity/preference.
# Models with higher weights will be selected more often.
MODELS = [
    {"name": "gemma-4-26b-a4b-it", "weight": 1.0},
    {"name": "gemma-4-31b-it", "weight": 1.0},
    {"name": "gemini-3.1-flash-lite", "weight": 0.25},
    {"name": "gemini-2.5-flash", "weight": 0.25},
    {"name": "gemini-3.5-flash", "weight": 0.25},
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            # Ensure current_model_index is valid for the new MODELS list
            if state["current_model_index"] >= len(MODELS):
                state["current_model_index"] = 0 # Reset if out of bounds
            return state
    return {"current_model_index": 0, "api_key_index": 0}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_current_model(state):
    # This logic assumes the API keys are managed external to this script,
    # and this script only rotates models for the *active* API key.
    # The actual API key rotation (if multiple are available) would need
    # to be handled by Hermes's credential pool after a model is exhausted.
    
    # Simple weighted round-robin for models
    total_weight = sum(m["weight"] for m in MODELS)
    current_weight_sum = 0
    
    # Calculate cumulative weights
    cumulative_weights = []
    for model in MODELS:
        current_weight_sum += model["weight"]
        cumulative_weights.append(current_weight_sum)

    # Find next model based on current index and cumulative weights
    # This ensures models with higher weights are more likely to be picked over time
    current_index = state["current_model_index"]
    
    # Simple round-robin for now, we can add more sophisticated weighted logic later
    next_index = (current_index + 1) % len(MODELS)
    state["current_model_index"] = next_index
    
    return MODELS[next_index]["name"]

def update_hermes_model(model_name):
    print(f"Attempting to set Hermes model to: {model_name}")
    try:
        # Use subprocess to run the hermes config command
        result = subprocess.run(
            ["hermes", "config", "set", "model.default", model_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Hermes config set output: {result.stdout}")
        if result.stderr:
            print(f"Hermes config set error: {result.stderr}")
        print(f"Successfully set Hermes model to {model_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error setting Hermes model to {model_name}: {e}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    state = load_state()
    next_model = get_current_model(state)
    update_hermes_model(next_model)
    save_state(state)
