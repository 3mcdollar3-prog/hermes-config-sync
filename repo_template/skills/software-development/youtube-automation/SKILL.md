---
name: youtube-automation
description: Workflows for downloading and uploading videos to YouTube using yt-dlp and custom Python upload scripts.
---

# YouTube Automation

This skill governs the pipeline of downloading content from social platforms (YouTube, Instagram, X) and uploading them to a target YouTube channel.

## Workflows

### 1. Downloading Media
- Use `yt-dlp` via the `video_downloader_webapp` or direct CLI.
- **Pitfall:** Instagram often serves fragmented DASH streams.
- **Fix:** Use `-f "bestvideo+bestaudio" --merge-output-format mp4` to ensure compatible files.

### 2. Uploading Videos
- Use the `upload_video.py` script located in `~/Desktop/video_upload3r/`.
- **Critical Step:** Always `cd` into the script directory before execution to ensure `client_secrets.json` and `token.json` are found via relative paths.
- **Command Pattern:** 
  `./venv/bin/python upload_video.py --file <path_to_video> --title "<title>" --privacyStatus <public|private|unlisted>`

## Pitfalls & Lessons
- **Format Compatibility:** Avoid using raw DASH outputs for WhatsApp delivery; always merge to standard H.264 MP4 for maximum device compatibility.
- **Pathing:** Remote execution of Python scripts relying on local `.json` credentials must be run from the script's working directory to avoid `FileNotFoundError`.
- **API Limits:** Be mindful of YouTube API quotas when performing bulk uploads.
