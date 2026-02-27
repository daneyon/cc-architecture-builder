---
name: publishing-video
description: Procedural knowledge for uploading a finished video to YouTube or other platforms. Use when the user invokes /publish-video.
---

# Publishing Video

## Overview

This skill provides the procedure for uploading a completed video with metadata to YouTube using the YouTube Data API v3 or manual upload guidance.

## Instructions

1. **Verify prerequisites** — Confirm video file and `output/metadata.json` exist
2. **Check upload method** — Determine if automated (API) or manual upload
3. **For automated upload** — Use the YouTube upload script if API credentials are configured
4. **For manual upload** — Provide step-by-step instructions with the metadata pre-filled
5. **Confirm upload** — Verify the video is accessible on the platform

## When to Apply

- A completed video and metadata exist in `output/`
- The user has invoked `/publish-video`
- The quality-reviewer has approved the output (or user has overridden)

## Automated Upload (if configured)

```bash
python3 scripts/upload-youtube.py \
  --video output/<video-name>.mp4 \
  --metadata output/metadata.json \
  --credentials providers/config.local.json
```

Requires:
- YouTube Data API v3 enabled in Google Cloud Console
- OAuth2 credentials in `providers/config.local.json`
- First run will prompt for browser-based authorization

## Manual Upload Guide

If automated upload isn't configured, provide this to the user:

1. Go to [YouTube Studio](https://studio.youtube.com)
2. Click "CREATE" → "Upload videos"
3. Select: `output/<video-name>.mp4`
4. Fill in from metadata.json:
   - Title: `{metadata.title}`
   - Description: `{metadata.description}`
   - Tags: `{metadata.tags}`
   - Category: `{metadata.category}`
5. Set visibility (recommend "Unlisted" for review, then "Public")
6. Click "Publish"

## Constraints

- Never store OAuth tokens in git-tracked files
- Use `providers/config.local.json` (gitignored) for credentials
- Default to manual upload instructions if no API credentials exist
- Always recommend "Unlisted" first for quality review before going public
