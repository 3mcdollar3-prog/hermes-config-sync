---
name: youtube-content-automation
description: Workflows for downloading and uploading YouTube/Instagram content for content repurposing pipelines.
---

# YouTube Content Automation

Guidelines for managing a content pipeline involving video downloads from social media and uploads to YouTube.

## Workflows

### High-Compatibility Video Downloading
When downloading Reels or Shorts that fail with standard 'best' quality settings:
1. Identify available formats using `yt-dlp --list-formats <URL>`.
2. If a single 'combined' mp4 isn't available, download the best video-only stream and best audio-only stream separately.
3. Merge them using `--merge-output-format mp4` to ensure a playable result.
4. If the resulting file doesn't play in WhatsApp/Gallery, it may need conversion to standard H.264 MP4.

### Automated YouTube Uploading
To upload videos using the existing `video_upload3r` tool:
1. Navigate to the tool directory: `/home/pr3cision/Desktop/video_upload3r`.
2. Execute using the project's virtual environment: `./venv/bin/python upload_video.py`.
3. Required arguments: `--file <path>`, `--title <title>`, `--privacyStatus <public|private|unlisted>`.
4. Ensure `client_secrets.json` and `token.json` are present in the working directory.

## Pitfalls
- **Working Directory:** The `upload_video.py` script expects `client_secrets.json` in the current working directory. Always `cd` into the project folder before executing.
- **yt-dlp Versions:** Instagram frequently changes its API; always check for `yt-dlp` updates if downloads suddenly fail.
- **Codec Compatibility:** DASH-merged files may not play natively on all mobile devices; verify the output is a standard MP4 if the user reports playback issues.
