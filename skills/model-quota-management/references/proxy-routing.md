---
name: proxy-routing
description: Detailed implementation methodology for building a local API proxy to manage model routing and rate limits.
---

# Proxy-Based Routing Implementation

This document details the methodology for building and managing a local proxy to handle intelligent model routing. 

## Core Concepts

- **Priority-Based Rotation:** Instead of just rotating API keys, the proxy rotates through a prioritized list of models (e.g., `gemini-3.5-flash` $\\rightarrow$ `gemini-2.5-pro`) to maximize the utilization of all available quotas.
- **Error-Triggered Switching:** The router actively listens for `429 Too Many Requests` or `RESOURCE_EXHAUSTED` errors. Upon detection, it immediately marks the current model as exhausted and retries the request with the next model in the priority list.
- **State Persistence:** The router maintains a `router_state.json` to remember which model is currently \"healthy\" across restarts.

## Implementation Workflow

1.  **Identify Priority List:** Define your models from highest capability/recency to lowest (e.g., `gemini-3.1-pro-preview` $\\rightarrow$ `gemini-2.5-flash-lite`).
2.  **Develop Proxy Script:** Use a lightweight framework like `Flask` to create a local endpoint that mimics the target provider's API structure.
3.  **Implement Error Logic:**
    - Catch `429` status codes.
    - Inspect response body for `RESOURCE_EXHAUSTED` strings.
    - Increment the \"current model index\" in the state file.
4.  **Configure Hermes:** Point the `model.base_url` in `config.yaml` to your local proxy address (e.g., `http://localhost:5000`).

## Pitfalls & Debugging

- **Timeout Mismatches:** Ensure the proxy timeout is longer than the underlying API's response time to avoid premature failures.
- **Endpoint Pathing:** When proxying, ensure the route handling (e.g., `/<path:model_path>`) correctly appaks the model name to the target provider's base URL.
- **Credential Access:** The proxy script needs access to the API keys (e.g., via `os.getenv`).

## Verification

To verify the router is working:
1. Start the router service.
2. Run a burst test using a dedicated testing script or a tool like `curl`.
3. Monitor the router logs (`router.log`) to see \"Model [NAME] hit rate limit. Trying next...\" messages.

## References
- [Session: Implementation of Gemini Model Rotation Proxy](/home/g33/api_tester_webapp.py)
