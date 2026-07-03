# Proactive Rate-Limit Router (Gemini)

When dealing with rate-limited APIs (like Google Gemini Free Tier), implementing proactive routing is more efficient than reactive retrying (429 handling).

## Strategy: Pre-flight Capacity Check

Instead of waiting for a 429:

1.  **Monitor usage**: Track `x-ratelimit-*` headers from previous responses.
2.  **Pre-flight check**: Before calling `run_conversation` or making an API request, query the `RateLimitTracker` (or custom capacity monitor).
3.  **Dynamic Routing**: If the tracker indicates the current model is at/near limit, automatically switch the `agent.provider` and `agent.model` to a fallback model or provider configured in the credential pool before the request is dispatched.
4.  **Integration Point**: Hook this into `agent/conversation_loop.py` immediately before the API pre-flight/request block.

## Implementation Details

- **Current Implementation**: `agent/nous_rate_guard.py` handles cross-session 429 recording.
- **Proposed Extension**: Implement `agent/proactive_router.py` to aggregate capacity state and expose `get_best_model()` to the main loop.
