# Smart Model Rotation State Tracking & Maintenance

The `smart_rotate.py` watchdog uses a state file to record API request timestamps, track daily/minute-level limits, and enforce automatic cooldowns for rate-limited models.

## State File Location
The tracking state is persisted in JSON format:
```bash
~/.hermes/scripts/model_state.json
```

## JSON Structure Overview
```json
{
  "usage": {
    "gemini-3.5-flash": {
      "requests": [
        1787968412.345,
        1787968455.678
      ],
      "daily_requests": 2,
      "daily_reset": 1787960000.0
    }
  },
  "cooldowns": {
    "gemma-4-31b-it": 1787969012.345
  },
  "last_index": 1,
  "last_handled_failure_time": "2026-08-29T02:21:45.516522+02:00"
}
```

### Fields Defined:
- `usage`: Maps each model to its list of Unix timestamps for requests made in the last 60 seconds (`requests`), the accumulated daily counter (`daily_requests`), and the daily epoch anchor (`daily_reset`).
- `cooldowns`: Maps models to the Unix timestamp when their 10-minute cooldown window expires.
- `last_index`: The index of the last active model in the credential pool strategies array.
- `last_handled_failure_time`: Prevents redundant cooldown cascading by storing the timestamp of the last handled watchdog job failure.

## Troubleshooting & State Maintenance

If a model is healthy but stuck in an active cooldown or rate-limiting state, you can inspect or reset the state:

### 1. View Current State File
To see the raw JSON state of all models:
```bash
cat ~/.hermes/scripts/model_state.json
```

### 2. Check Active Status
Run the script status command to get a human-readable summary of RPM, RPD, TPM, and cooldown status:
```bash
/home/mcdollar3/.hermes/venv_stt/bin/python3 ~/.hermes/scripts/smart_rotate.py status
```

### 3. Clear/Reset All Quotas and Cooldowns
To completely clear the tracking state and force-reset all cooldowns:
```bash
rm ~/.hermes/scripts/model_state.json
```
The watchdog script will automatically re-initialize an empty state file with all models healthy on its next execution or rotation trigger.

### 4. Manually Remove Cooldown for a Specific Model
To remove a cooldown for a single model while keeping other usage history:
1. Open `~/.hermes/scripts/model_state.json`.
2. Under `"cooldowns"`, delete the entry for the target model or set its epoch value to `0`.
