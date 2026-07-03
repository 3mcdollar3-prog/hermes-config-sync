---
name: video-content-automation
description: Skills for downloading, processing, and managing video content from social platforms (YouTube, Instagram, X).
category: software-development
---

# Video Content Automation

Skills for downloading, processing, and managing video content from social platforms (YouTube, Instagram, X).

## Core Workflows

### Downloading from Social Platforms
When using `yt-dlp` based tools (like the user's local webapp):
1. **Verify Environment**: Ensure the correct virtual environment is active if running via terminal (e.g., `/path/to/venv/bin/python`).
2. **Format Handling**:
   - For YouTube: Standard `bestvideo+bestaudio` usually works.
   - For Instagram: If a standard download fails with "Requested format not available", the video and audio are likely separated as DASH streams. Use a manual merge command:
     `yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" --merge-output-format mp4 -o "filename.mp4" [URL]`
3. **Compatibility**: Use H.264 MP4 for maximum compatibility across WhatsApp and mobile galleries to avoid "file cannot be played" errors.

## Pitfalls & Troubleshooting
- **Port Conflicts**: The video downloader webapp typically runs on port 5000. If connection fails, check `ss -tuln | grep 5000`.
- **PO Tokens**: YouTube may block automated downloads with "GVS PO Token" errors. This requires updated `yt-dlp` versions or specific extractor args (`--extractor-args "youtube:player_client=android"`).
- **Instagram Rate Limits**: Instagram is highly sensitive to scraping. If downloads fail repeatedly, allow a cooldown period or try different quality flags.

## Verification
- Check file size and extension.
- For merged files, verify it isn't just an audio stream (which happens if the video stream is missing/blocked).
