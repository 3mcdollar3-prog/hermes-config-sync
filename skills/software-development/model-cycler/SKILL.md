---
name: model-cycler
description: "Rotates the active Hermes model to exhaust specific rate limits."
---

# Model Cycler

This skill automates switching between high-throughput Gemini models to maximize API quota efficiency.

## Usage

```bash
# Switch to the next model in the rotation list
hermes skills run model-cycler
```

## Rotation List (Edit to change order)
1. gemini-3.1-flash-lite
2. gemini-2.5-flash
3. gemini-3.5-flash
4. gemini-3.1-pro-preview
5. gemini-3.1-flash
6. gemini-2.5-pro

## Troubleshooting & Pitfalls
- **Gemini Free Tier Quota Sharing**: Model aliases (like `gemini-flash-latest`) and their underlying models (like `gemini-3.5-flash`) often share the same free tier request limit (typically 20 RPM/250 RPD). Switching to an alias of the same model will not bypass rate limits if the limit is set at the metric level.
- **Resource Exhausted (429) Errors**: Inspect `~/.hermes/logs/errors.log` and `~/.hermes/logs/agent.log` for `RESOURCE_EXHAUSTED` or `generate_content_free_tier_requests` error messages.
- **Native Rotation Config**: To ensure native rotation is seamless, `api_max_retries` should be set to at least 5 in `~/.hermes/config.yaml` to allow the engine to try multiple rotated models from the pool before raising a failure.

## Implementation
This skill uses `hermes config set` to define a rotation list in `credential_pool_strategies`, which allows the Hermes core engine to natively rotate models on rate limits (429) without needing external scripts or gateway restarts.

## Configuration (Native Engine Integration)
To enable native rotation for Gemini models, ensure your `~/.hermes/config.yaml` includes:

```yaml
credential_pool_strategies:
  gemini:
    rotation: round_robin
    models:
      - gemini-3.1-flash-lite
      - gemini-2.5-flash
      - gemini-3.5-flash
      - gemini-3.1-pro-preview
      - gemini-3.1-flash
      - gemini-2.5-pro
```
And ensure retries are set to handle the rotation window:
```yaml
agent:
  api_max_retries: 5
```
