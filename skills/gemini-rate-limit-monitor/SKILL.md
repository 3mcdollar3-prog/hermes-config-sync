---
name: gemini-rate-limit-monitor
description: "Monitors and enforces rate limits based on Google AI Studio dashboard observations."
tags: [gemini, rate-limits, quotas, monitoring]
---

# Gemini Rate Limit Monitor

This skill provides a mechanism to map observed rate limits from the Google AI Studio dashboard into a configuration that Hermes Agent can use to proactively switch models.

## How to use

1.  **Extract Data:** Use the dashboard screenshots (provided earlier) to populate the `model_limits.json` file.
2.  **Configuration:** The monitor uses a JSON map of model IDs to their daily/minute limits.
3.  **Proactive Switching:** The Hermes Agent `conversation_loop` will consult this map before making an API call. If a model is approaching its limit, it will automatically switch to the next available model in the priority list.

## Data Schema (model_limits.json)

```json
{
  "gemini-2.5-flash": {
    "requests_per_day": 30,
    "tokens_per_minute": 1000000,
    "requests_per_minute": 15
  },
  "gemini-2.5-pro": {
    "requests_per_day": 50,
    "tokens_per_minute": 32000,
    "requests_per_minute": 2
  }
}
```

## Implementation

The logic is injected into `agent/conversation_loop.py` to intercept requests before they are sent.

## Pitfalls

- **Stale Data:** Limits shown in the dashboard may change if you upgrade your tier. Update the JSON file whenever you see "Quota Exceeded" warnings in the dashboard.
- **Provider Latency:** Switching models might take a few seconds, which is reflected in the agent's turn latency.
