---
name: voice-setup-troubleshooting
description: Guide for configuring Speech-to-Text (STT) and Text-to-Speech (TTS) in Hermes Agent, specifically handling Linux environment constraints and package management.
tags: [stt, tts, faster-whisper, linux, troubleshooting]
---

# Voice Setup & Troubleshooting

This skill provides a workflow for enabling and debugging the voice capabilities of Hermes Agent.

## 1. Text-to-Speech (TTS) Setup
TTS is typically easier to enable. If the user has the `edge-tts` library installed, this can be activated in the config.

## 2. Speech-to-Text (STT) Setup
STT allows the agent to "hear" voice notes. There are two primary paths:

### Path A: Cloud API (Recommended)
Using a provider like Groq or OpenAI Whisper.
- **Pros:** Instant setup, high accuracy, low resource usage.
- **Process:**
  1. Obtain API key from provider (e.g., console.groq.com).
  2. Set the provider in `config.yaml` or via `hermes config set stt.provider <provider>`.
  3. Set the API key.
  4. Enable STT: `hermes config set stt.enabled true`.

### Path B: Local Installation (`faster-whisper`)
Use this when API keys are unavailable or privacy is paramount.
- **Pros:** Free, private, no API keys.
- **Cons:** Heavy installation, higher CPU/RAM usage, slower transcription.

**Installation Workflow (Linux):**
1. **Install Package:** Use `pip install faster-whisper`.
2. **Handle PEP 668:** In modern Linux environments (like Debian/Ubuntu), `pip` may block system-wide installs.
   - **Fix:** Use `--break-system-packages` flag if installing in a controlled agent environment where system stability is managed by the agent.
   - **Alternative:** Create a dedicated virtual environment (`python3 -m venv venv`).
3. **Configure:** `hermes config set stt.enabled true`.
4. **Apply:** Restart the Hermes gateway.

## 🛠 Pitfalls & Troubleshooting

### The "Mirror" Loop (Digital Echo)
**Symptom:** The agent starts echoing its own internal reasoning, timeouts, and system logs (`⚡ Interrupting current task`, `Operation interrupted`) back to the user as if they were user messages.
**Cause:** This is typically a frontend/interface glitch where internal state is leaked into the chat stream.
**Resolution:** 
- Stop engaging with the "AI-style" mirrored text.
- Ask the user for a "Human Verification" signal (a random word like "Banana").
- If it persists, advise the user to refresh the page, restart the app, or clear the session cache.

### Installation Timeouts
**Symptom:** `pip install` fails with a timeout (exit code 124) during the installation of large wheels (like `ctranslate2` or `onnxruntime`).
**Resolution:** Re-run the installation command. Large ML packages often time out on slower connections or restricted environments.

## Verification
To verify "ears" are working:
- User sends a voice note.
- Agent should produce a transcription that does NOT rely on platform-provided metadata (i.e., the agent's own STT tool logs should show activity).
