---
name: youtube-content-repurposing
description: "Workflow for downloading, analyzing, and repurposing YouTube content into new styles (e.g., Adala-style) using vision models and transcription."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# YouTube Content Repurposing

This skill governs the end-to-end process of transforming existing YouTube videos into a new format or persona. 

## Workflow

1. **Target Identification**: Identify the source channel or specific video URLs.
2. **Stealth Acquisition**: Use `yt-dlp` with authentication cookies to bypass bot detection.
3. **Content Analysis**: 
   - Use `video_analyze` to extract visual cues and scene transitions.
   - Fetch transcripts for textual context.
4. **Stylistic Transformation**: 
   - Map the original content to the target persona's tone, pacing, and "hooks."
   - Create a structured script with precise timestamps.
5. **Deliverable Generation**: Produce a final package containing:
   - Optimized Titles (Click-through focused).
   - Script with timestamps for editing.
   - Visual/Audio notes for the repurposing phase.

## Pitfalls & Technical Notes

- **Bot Detection**: YouTube aggressively blocks data-center IPs and generic `yt-dlp` fingerprints. **Always use `--cookies`** exported from a real browser session in Netscape format, or utilize the `--extractor-args \"youtube:player_client=android\"` flag to bypass some JS runtime requirements. Note that playlists may still fail due to PO Token requirements or unavailable videos; in such cases, download videos individually. **X/Twitter is also supported by yt-dlp and can be downloaded using similar methods.**
- **Cookie Format**: `yt-dlp` does not accept JSON cookies. They must be converted to Netscape text format.
- **Environment Isolation**: When using specific toolsets like `yt-dlp`, check for existing virtual environments on the system that may have pre-installed dependencies or specialized versions.

## Verification
- Ensure the downloaded video is the correct length and quality.
- Verify that the repurposed script aligns with the target persona's known style.
