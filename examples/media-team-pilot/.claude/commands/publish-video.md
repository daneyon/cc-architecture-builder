---
description: Prepare or upload a finished video to YouTube or other platforms
allowed-tools: Read, Bash, Write
---

# Publish Video

Prepare a finished video for platform publishing, with automated upload if API credentials are configured, or manual upload guidance otherwise.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `$1` | No | Platform target (defaults to "youtube") |
| `$ARGUMENTS` | No | Full argument string for additional options |

## Behavior

1. **Verify deliverables exist**:
   - Check `output/` for .mp4 file
   - Check `output/metadata.json` exists
   - If either missing, suggest running `/create-video` or `/review-video` first

2. **Check for API credentials**:
   - Look for `providers/config.local.json` with YouTube API credentials
   - Check for `YOUTUBE_API_KEY` environment variable

3. **If automated upload available**:
   - Run the upload script with metadata
   - Report the video URL when complete
   - Recommend starting as "Unlisted" for review

4. **If manual upload (default)**:
   - Display the metadata in a copy-paste friendly format
   - Provide step-by-step upload instructions for the target platform
   - Include all metadata fields formatted for the platform

## Manual Upload Output

```
## Ready to Publish

### Video File
output/<video-name>.mp4

### Copy-Paste Metadata

**Title:**
<title from metadata.json>

**Description:**
<description from metadata.json>

**Tags:**
<comma-separated tags>

**Category:**
<category>

### Upload Steps (YouTube)
1. Go to YouTube Studio → Create → Upload videos
2. Select the video file listed above
3. Copy the title, description, and tags above
4. Set visibility to "Unlisted" for initial review
5. Publish, then review before making "Public"
```
