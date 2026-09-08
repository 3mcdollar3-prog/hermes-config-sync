# Gemini Credential Pool and Model Rotation Behavior

## Current Behavior
The Hermes Agent's `credential_pool.py` is designed to manage and rotate API keys for a given provider (e.g., Gemini). When multiple API keys are configured for a provider, the system will cycle through these keys based on the configured strategy (e.g., round-robin, least-used) and mark a key as "exhausted" if it encounters errors (e.g., rate limits, authentication failures).

However, the current implementation *does not* inherently support rotating through multiple *models* associated with a single API key before moving to the next API key in the pool. If a single API key has access to multiple Gemini models (e.g., `gemini-2.5-flash`, `gemini-1.5-pro`), the system will typically default to a single specified model (`model.default` in `config.yaml`) and only switch API keys when the current key is exhausted, not after iterating through all models available to that key.

## Implementing Model-then-Key Rotation
To achieve a "rotate all models with current key first, then move to next key" behavior, modifications to the Hermes Agent's core codebase are required. This is not achievable through configuration alone.

The primary areas for modification would be:

1.  **`agent/credential_pool.py`**:
    *   **Enhance `PooledCredential`**: Add a field to the `PooledCredential` dataclass to store a list of models associated with that specific API key, along with a `last_used_model_index` or similar to track the current model in rotation for that key.
    *   **Modify `_select_unlocked` or add a new model selection method**: When a credential is acquired, this method would need to:
        *   Determine the next model to use from the credential's model list based on the `last_used_model_index`.
        *   Increment `last_used_model_index` (and loop back to the start if it reaches the end of the list).
        *   Only if all models for the current `PooledCredential` have been exhausted (or cycled through) should the `credential_pool` proceed to select the next *API key*.

2.  **`agent/gemini_native_adapter.py` and/or model routing logic**:
    *   The `gemini_native_adapter.py` is responsible for translating OpenAI-style requests to native Gemini API calls. It would need to be updated to accept the dynamically selected model from the `credential_pool` and use it in the `generateContent` request.
    *   Higher-level model routing logic (potentially in `run_agent.py` or another routing module if it existed) would need to be aware of this new model rotation strategy when requesting a model from the `credential_pool`.

## Steps for Code Modification
1.  **Add `models: List[str]` and `last_used_model_idx: int` to `PooledCredential` in `agent/credential_pool.py`**.
2.  **Modify `CredentialPool._select_unlocked` (or a new helper function)** to manage the `last_used_model_idx` for the selected `PooledCredential` and cycle through its `models` list before delegating to the next `PooledCredential` in the overall pool.
3.  **Ensure the selected model is passed to the Gemini API adapter**. The `gemini_native_adapter.py`'s `build_gemini_request` function will need to use this specific model.

This approach ensures that all models within a single API key are utilized before the system attempts to switch to another API key in the credential pool, providing more granular control over model usage and potentially optimizing API key consumption.