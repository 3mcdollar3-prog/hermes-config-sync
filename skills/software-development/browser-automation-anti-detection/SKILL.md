---
name: browser-automation-anti-detection
description: "Strategies for automating web interactions on platforms with aggressive bot detection (e.g., X/Twitter, LinkedIn)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [automation, anti-detection, browser, mcp, cdp]
---

# Browser Automation & Anti-Detection

Interacting with high-security platforms (like X/Twitter) often leads to login walls, CAPTCHAs, or "bot detection" redirects, even when using authentic cookies. This skill provides the hierarchy of approaches from least to most reliable.

## Hierarchy of Approaches

### 1. The "Golden Path": Remote Debugging (Highest Reliability)
When a platform has aggressive fingerprinting, don't simulate a browser—control the user's actual browser.
- **Mechanism:** Launch Chrome with `--remote-debugging-port=9222`.
- **Why it works:** The agent uses the actual browser process, including the user's real cookies, hardware fingerprints, and established session.
- **Pitfall:** All existing Chrome instances must be killed first for the port to open.
- **Verification:** Test connection via `http://localhost:9222/json/list`.

### 2. Session Injection (Medium Reliability)
Injecting `auth_token` and `ct0` (CSRF) cookies into a headless or automated session.
- **Mechanism:** Use browser tools to set cookies before navigating.
- **Pitfall:** Fingerprint mismatch. X often detects that the `User-Agent` or hardware profile of the bot doesn't match the session associated with the cookies.

### 3. Headless Automation (Lowest Reliability)
Using Playwright/Puppeteer with "stealth" plugins.
- **Mechanism:** Standard automation tools.
- **Pitfall:** High risk of "Bot Detection" walls and CAPTCHAs.

## Pitfalls & Troubleshooting

- **Connection Refused (Port 9222):** This almost always means the `--remote-debugging-port` flag was ignored because a background Chrome process was already running. Use `pkill chrome` or end all tasks in Task Manager.
- **Login Redirects:** If you are redirected to `/login` despite having cookies, the session is being invalidated due to a fingerprint mismatch. Switch to Remote Debugging.
- **Tool Timeouts:** Large-scale MCP server calls to browsers can timeout. Consider using direct CDP requests via `requests` and `websockets` for more granular control.

## Implementation Flow
1. Attempt public access.
2. If blocked, try Cookie Injection (if tokens are available).
3. If still blocked, request the user to launch with `--remote-debugging-port=9222`.
4. Use `json/list` to find the target tab and `Runtime.evaluate` to inject JS actions.
