---
name: model-quota-management
description: "Strategies and implementations for managing model quotas and rate limits (e.g., proxy-based routing or scheduled rotation)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [quota, rate-limit, rotation, proxy, api]
---

# Model Quota & Rate Limit Management

This skill provides a collection of methodologies for maximizing model availability and bypassing rate limits (e.g., `429 Too Many Requests`) through intelligent routing and rotation strategies.

## Overview of Strategies

Different environments and requirements call for different approaches:

### 1. Proxy-Based Routing
This approach involves running a local or centralized proxy that intercepts API calls and routes them to different models or API keys based on availability and priority.
- **Best for:** Real-time applications requiring minimal latency and seamless fallback.
- **Details:** See [Proxy-Based Routing Implementation](references/proxy-routing.md).

### 2. Scheduled/Scripted Rotation
This approach uses a background process (e.g., a cron job) to periodically update the active model or API key used by the agent.
- **Best for:** Batch processing or scenarios where a short delay in switching models is acceptable.
- **Details:** See [Gemini Model Rotation Strategy](references/gemini-rotation.md).

## Pitfalls & Debugging

- **Latency:** Proxies add a hop. Ensure timeouts are configured correctly.
- **State Consistency:** If using rotation, ensure the state (which model is currently exhausted) is persisted across restarts.
- **Error Detection:** Ensure the implementation correctly identifies `429` or `RESOURCE_EXHAUSTED` errors.

## Verification

- Monitor logs for "Model exhausted" or "Switching to..." messages.
- Use burst tests to trigger rate limits and observe the fallback mechanism.
