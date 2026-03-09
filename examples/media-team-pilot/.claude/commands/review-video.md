---
description: Review an existing video output and get improvement suggestions
allowed-tools: Read, Bash, Grep, Glob
---

# Review Video

Review a previously produced video and provide detailed feedback.

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `$1` | No | Path to the video file (defaults to most recent in output/) |

## Behavior

1. **Find the video** — If no path given, find the most recent .mp4 in `output/`
2. **Inspect with ffprobe** — Get technical details (duration, resolution, codec, streams)
3. **Read the script** — If `temp/script.json` exists, compare intended vs actual
4. **Read existing metadata** — If `output/metadata.json` exists, review it
5. **Provide comprehensive review**:
   - Technical quality assessment
   - Content alignment with original brief
   - Metadata quality for platform publishing
   - Specific improvement suggestions

## Output

Present findings as:

```
## Video Review

### Technical Details
- File: ...
- Duration: ...
- Resolution: ...
- Codecs: ...
- File size: ...

### Content Assessment
- Scene count: ...
- Narration quality: ...
- Visual cohesion: ...

### Metadata Review
- Title effectiveness: ...
- Description SEO quality: ...
- Tag coverage: ...

### Improvement Suggestions
1. ...
2. ...
3. ...
```
