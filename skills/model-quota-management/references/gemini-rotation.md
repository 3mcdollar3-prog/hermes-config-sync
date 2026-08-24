---
name: gemini-rotation
description: Detailed strategy and implementation for automated, weight-based Gemini model rotation via cron jobs.
---

# Gemini Model Rotation Strategy

This document details the strategy for rotating between Google Gemini models to maximize inference capacity across different models (Flash, Pro, Gemma) and their respective rate limits.

## Strategy

Instead of exhausting a single model's quota, we cycle through a validated sequence of models. This ensures continuous service and leverages the specific throughput advantages of each model tier, using **weights** to account for differing capacity limits (Flash vs. Thinking models).

## Sequence & Models in Pool

The configured model pool typically consists of the following Gemini/Gemma models in order of priority:
1. `gemini-3.6-flash`
2. `gemini-3.5-flash`
3. `gemini-3.1-flash`
4. `gemini-3.1-flash-lite`
5. `gemini-3.1-pro-preview`
6. `gemini-2.5-flash`
7. `gemini-2.5-pro`
8. `gemma-4-26b-a4b-it`
9. `gemma-4-31b-it`

## Implementation

The rotation is managed via automated cron jobs using a Python-based rotation watchdog script.

### Quota-Aware Python Script (`~/.hermes/scripts/smart_rotate.py`)
This script implements advanced, limit-aware rotation. It parses `~/.hermes/config.yaml` to fetch the credential pool models, tracks rate limits, and persists its state in `~/.hermes/scripts/model_state.json`.

#### Key Features:
- **Rate-Limit Enforcement:** Integrates official Google Model limits (RPM, TPM, RPD) for each model (e.g., Flash limits, Gemma limits).
- **Auto-Failure Detection:** Parses `~/.hermes/cron/jobs.json` to check if previous runs of the watchdog failed with standard HTTP 429/Resource Exhausted errors. If detected, it automatically places the failed model on a 10-minute cooldown.
- **Explicit Cooldowns:** Temporarily takes rate-limited models out of the rotation sequence.

#### CLI Usage:
- **Show Status:** Displays current model status (Healthy, Cooldown, Quota Exceeded), RPM/RPD usage, and active models.
  ```bash
  python3 ~/.hermes/scripts/smart_rotate.py status
  ```
- **Force Rotation:** Forces the active model to shift to the next candidate in the pool regardless of current usage (though still respecting active cooldowns unless forced).
  ```bash
  python3 ~/.hermes/scripts/smart_rotate.py force
  ```
- **Mark Fail:** Marks a specific model as failed and puts it on a 10-minute cooldown, then triggers a rotation.
  ```bash
  python3 ~/.hermes/scripts/smart_rotate.py fail <model_name>
  ```
- **Record Request:** Logs a request timestamp for the specified model to keep usage counters accurate.
  ```bash
  python3 ~/.hermes/scripts/smart_rotate.py record <model_name>
  ```

### Simple Sequential Script (`~/.hermes/scripts/rotate.sh`)
A basic bash-based alternative that loops sequentially through the model array using the `hermes config` command to update `model.default` without tracking rate limits or cooldown state.

### Automation (`cronjob`)
The rotation is scheduled via a local cron job:
```bash
hermes cron create \"every 5m\" --script \"rotate.sh\"
```

## Verification

- Use `hermes config` to verify the active `model.default`.
- Use `hermes cron list` to verify rotation job status.
- Ensure model IDs match the output of `https://generativelanguage.googleapis.com/v1beta/models`.
