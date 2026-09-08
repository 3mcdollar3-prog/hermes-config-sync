---
name: website-to-pdf
description: Use when converting web pages or URLs into PDF files.
version: 1.0.0
author: Hermes Agent
---

# Website to PDF Pipeline

This skill converts web URLs into high-quality rendered PDF documents using headless Chromium and delivers them directly via platform media attachments.

## Workflow

1. Ensure the output directory exists:
   ```bash
   mkdir -p /home/mcdollar3/web_pdfs
   ```

2. Render the target URL to PDF using full desktop user-agent headers to avoid locale redirects, bot blocks, or blank pages:
   ```bash
   chromium --headless --disable-gpu --no-sandbox --disable-dev-shm-usage \
     --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" \
     --window-size=1920,1080 \
     --virtual-time-budget=5000 \
     --print-to-pdf="/home/mcdollar3/web_pdfs/<filename>.pdf" "<URL>"
   ```

3. Deliver the resulting PDF file to the chat using media attachment syntax:
   `MEDIA:/home/mcdollar3/web_pdfs/<filename>.pdf`
