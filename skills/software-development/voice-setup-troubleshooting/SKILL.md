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
  1. Obtain API key from provider (e.g., [console.groq.com](https://console.groq.com/)).
  2. Configure provider:
     ```bash
     hermes config set stt.provider <provider> # e.g., groq
     hermes config set stt.<provider>.model <model_name> # e.g., whisper-large-v3
     ```
  3. Add API key to `~/.hermes/.env` (e.g., `GROQ_API_KEY=...`).
  4. Enable STT: `hermes config set stt.enabled true`.

### Path B: Local Installation (`faster-whisper`)
Use this when API keys are unavailable or privacy is paramount.
- **Pros:** Free, private, no API keys.
- **Cons:** Heavy installation, higher CPU/RAM usage, slower transcription.

## Installation Workflow (Linux)
1. **Install Package:** Use `pip install faster-whisper`.
2. **Handle PEP 668:** In modern Linux environments (like Debian/Ubuntu), `pip` may block system-wide installs.
   - **Fix 1:** Use `python3 -m pip install` within the local virtual environment.
   - **Fix 2:** If the environment is a venv, ensure you are using the specific venv's pip: `/path/to/venv/bin/pip3 install faster-whisper`.
   - **Note:** If installation times out (e.g., exit code 124 for large packages like `ctranslate2` or `onnxruntime`), re-run the command; it will resume or use cached files to complete.
3. **Configure:** `hermes config set stt.enabled true`.
4. **Apply:** Restart the Hermes gateway.

### Pitfalls when driving
- **Driving/Safety Interaction:** When interacting with an agent while driving, users cannot safely read long text responses. 
- **Requirement:** Ensure all multi-paragraph or complex status updates are automatically followed by an Edge TTS (`text_to_speech`) call.
- **Verification:** Always acknowledge that the user should "stay focused on the road" and deliver a compact text summary first, followed by the audio.

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
