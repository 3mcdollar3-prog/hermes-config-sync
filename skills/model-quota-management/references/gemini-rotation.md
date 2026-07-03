---
name: gemini-rotation
description: Detailed strategy and implementation for automated, weight-based Gemini model rotation via cron jobs.
---

# Gemini Model Rotation Strategy

This document details the strategy for rotating between Google Gemini models to maximize inference capacity across different models (Flash, Pro, Gemma) and their respective rate limits.

## Strategy

Instead of exhausting a single model's quota, we cycle through a validated sequence of models. This ensures continuous service and leverages the specific throughput advantages of each model tier, using **weights** to account for differing capacity limits (Flash vs. Thinking models).

## Sequence & Weights

1. gemini-3.1-flash-lite (Weight 1.0)
2. gemini-2.5-flash (Weight 1.0)
3. gemini-3.5-flash (Weight 1.0)
4. gemma-4-26b-a4b-it (Weight 0.25)
5. gemma-4-31b-it (Weight 0.25)

## Implementation

The rotation is managed by an automated cron job and a Python-based rotation script.

### Quota-Aware Script (`~/.hermes/scripts/rotate.sh`)
The script uses a weight-based rotation system and persists its state in `~/.hermes/scripts/model_state.json` to track usage index across sessions and system restarts.

### Automation (`cronjob`)
The rotation is scheduled via a local cron job:
```bash
hermes cron create \"every 5m\" --script \"rotate.sh\"
```

## Verification

- Use `hermes config` to verify the active `model.default`.
- Use `hermes cron list` to verify rotation job status.
- Ensure model IDs match the output of `https://generativelanguage.googleapis.com/v1beta/models`.
