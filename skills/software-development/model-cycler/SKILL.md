---
name: model-cycler
description: \"Rotates the active Hermes model to exhaust specific rate limits.\"
---

# Model Cycler

This skill automates switching between high-throughput Gemini models to maximize API quota efficiency.

## Usage

```bash
# Switch to the next model in the rotation list
hermes skills run model-cycler
```

## Rotation List (Prioritized for Quota Recovery)
1. gemma-4-26b-a4b-it
2. gemma-4-31b-it
3. gemini-2.5-flash
4. gemini-2.5-pro
5. gemini-3.1-flash
6. gemini-3.1-flash-lite
7. gemini-3.1-pro-preview

## Fallback Provider Chain
When all Google API keys and their model rotations are exhausted, Hermes falls back to Ollama Cloud:
```yaml
fallback_providers:
  - provider: ollama-cloud
    model: gemma4:31b-cloud
```

## Architecture: Google Primary → Model Rotation → Key Rotation → Ollama Fallback
This skill implements the user's specified fallback hierarchy:

1. **Primary Provider**: Google (gemini) via `credential_pool_strategies.gemini`
2. **Model Rotation**: Round-robin through prioritized models (Gemma first) on *each* API key
3. **Key Rotation**: When all models on a key exhaust quota (429/usage_limit_reached), pool rotates to next API key
4. **Emergency Fallback**: When *all* Google keys exhausted, `fallback_providers` chain activates → Ollama Cloud

## Troubleshooting & Pitfalls
- **Default Script Execution Rotates State**: Running `python3 ~/.hermes/scripts/smart_rotate.py` with no arguments triggers an unconditional model rotation to the next candidate. To check status, verify limits, or inspect health *without* shifting the active model configuration, always pass the `status` argument explicitly: `python3 ~/.hermes/scripts/smart_rotate.py status`.
- **Gemini Free Tier Quota Sharing**: Model aliases (like `gemini-flash-latest`) and their underlying models (like `gemini-3.5-flash`) often share the same free tier request limit. Switching to an alias of the same model will not bypass rate limits if the limit is set at the metric level.
- **Resource Exhausted (429) Errors**: Inspect `~/.hermes/logs/errors.log` and `~/.hermes/logs/agent.log` for `RESOURCE_EXHAUSTED` or `generate_content_free_tier_requests` error messages.
- **Native Rotation Config**: To ensure native rotation is seamless, `api_max_retries` should be set to at least 5 in `~/.hermes/config.yaml` to allow the engine to try multiple rotated models from the pool before raising a failure.
- **Ollama Cloud Quota**: Ollama Cloud has a small quota (emergency backup only). Use `fill_first` strategy (configured in `credential_pool_strategies.ollama-cloud`) so it stays unused until explicitly needed.
- **Credential Pool Seeding**: Multiple Google API keys must be added via `hermes auth add gemini` (or `GOOGLE_API_KEY` / `GEMINI_API_KEY` in `.env`) to enable key rotation. The pool auto-seeds from env vars with sources `env:GOOGLE_API_KEY`, `env:GEMINI_API_KEY`.

## Smart Watchdog Integration (`smart_rotate.py`)
For automated, limit-aware model rotation, Hermes uses a cron-based watchdog (`smart-model-rotation-watchdog`) running every 5 minutes. The watchdog executes `~/.hermes/scripts/smart_rotate.py`, which:
- **Tracks RPM and RPD Limits**: Enforces official Google API limits (e.g., 5 RPM/20 RPD for Gemini 3.5/3.6 Flash, 15 RPM/500 RPD for Lite models) to prevent rate limits.
- **Automated Cooldowns**: Puts rate-limited or failed models on a 10-minute cooldown window.
- **Fail-Safe Historical Error Analysis**: Inspects `~/.hermes/cron/jobs.json` to check if a previous execution failed with a `429` or `RESOURCE_EXHAUSTED` error, applying cooldowns automatically. It compares timestamps (`last_run_at`) to avoid repeated cascading cooldowns of healthy models on consecutive watchdog runs.
- **Watchdog Pre-Run Recovery**: When an agent-driven cron job fails with a 429 error, the next watchdog execution parses `~/.hermes/cron/jobs.json` during the pre-run check, automatically applies a 10-minute cooldown to the failed model, and shifts the configuration to a healthy model before the agent session launches. This prevents back-to-back failures on the same rate-limited model.

A detailed tracking and state maintenance guide can be found in [references/smart-rotate-state-tracking.md](references/smart-rotate-state-tracking.md).

### Useful Watchdog Commands
```bash
# Check the current active model and quota tracking status
python3 ~/.hermes/scripts/smart_rotate.py status

# Force model rotation
python3 ~/.hermes/scripts/smart_rotate.py force

# Record a mock request to track rate limits for a model
python3 ~/.hermes/scripts/smart_rotate.py record <model_name>

# Mark a model as failed and place on 10-min cooldown
python3 ~/.hermes/scripts/smart_rotate.py fail <model_name>
```

## Implementation
This skill uses `hermes config set` to define a rotation list in `credential_pool_strategies`, which allows the Hermes core engine to natively rotate models on rate limits (429) without needing external scripts or gateway restarts. The fallback chain is configured via `fallback_providers` in config.yaml.

## Configuration (Native Engine Integration)
To enable native rotation for Gemini models with Ollama fallback, ensure your `~/.hermes/config.yaml` includes:

```yaml
model:
  provider: gemini
  default: gemini-2.5-flash
  base_url: https://generativelanguage.googleapis.com/v1beta/openai/

fallback_providers:
  - provider: ollama-cloud
    model: gemma4:31b-cloud

credential_pool_strategies:
  ollama-cloud: fill_first
  gemini:
    rotation: round_robin
    models:
      - gemma-4-26b-a4b-it
      - gemma-4-31b-it
      - gemini-2.5-flash
      - gemini-2.5-pro
      - gemini-3.1-flash
      - gemini-3.1-flash-lite
      - gemini-3.1-pro-preview

agent:
  api_max_retries: 5
```

## Adding Multiple Google API Keys
```bash
# Add first key
export GOOGLE_API_KEY=key1
hermes auth add gemini --label \"google-key-1\"

# Add second key 
export GOOGLE_API_KEY=key2
hermes auth add gemini --label \"google-key-2\"

# Or add via ~/.hermes/.env (auto-seeded on startup)
echo \"GOOGLE_API_KEY=key1\" >> ~/.hermes/.env
echo \"GEMINI_API_KEY=key2\" >> ~/.hermes/.env
```
