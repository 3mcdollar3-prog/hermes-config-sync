---
name: content-repurposing-automation
category: software-development
description: Skills for automating the collection, processing, and repurposing of content from social media and technical news sources.
---

# Content Repurposing & Automation

Skills for automating the collection, processing, and repurposing of content from social media and technical news sources.

## Triggers
- User wants to monitor news feeds or social media for specific topics.
- User wants a recurring summary report (e.g., Daily/Weekly Dev Briefs).
- User needs videos downloaded from YouTube, Instagram, or Twitter for repurposing.

## Workflows

### Recurring News Reports
1. **Source Selection**: Use a diverse mix of community hubs (Hacker News, Dev.to), industry news (TechCrunch), and official engineering blogs (GitHub, AWS).
2. **Scheduling**: Use `cronjob` to automate fetching.
3. **Formatting for WhatsApp**:
    - Start with a clear header (e.g., 🚀 DAILY DEV BRIEF).
    - Use a list format with emojis for readability.
    - Include: Catchy Title $\rightarrow$ 1-sentence summary $\rightarrow$ URL.
    - Embed images using `![alt](url)` to ensure they render as native photos on WhatsApp.

### Video Downloading (via `video_downloader_webapp`)
1. **App Lifecycle**: Ensure the Flask app is running in the background using the specific venv python: `/home/pr3cision/Desktop/video_downloader_webapp/venv/bin/python`.
2. **Request Pattern**: Use `curl` POST requests to `http://127.0.0.1:5000/download_youtube` with JSON body containing `url`, `quality`, and `format`.
3. **Format Handling**:
    - If `.mp4` fails (common on Instagram Reels), try `.mp3` as a fallback to at least capture the audio.
    - Use `quality: "best"` as the default.
4. **File Retrieval**: Locate the file in the `downloads/<download_id>/` directory using `find` and deliver via `MEDIA:/path/to/file`.

## Pitfalls & Troubleshooting
- **Port 5000 Connection**: If `curl` fails with "Failed to connect", the Flask app has likely crashed or not started. Check `process` logs and restart using the absolute venv path.
- **Instagram Format Errors**: Instagram often rejects specific format requests. If "Requested format is not available", fallback to audio or different quality settings.
- **YouTube PO Tokens**: Playlists may fail due to YouTube's PO Token requirements. Fall back to downloading individual videos via direct links.
