---
name: generating-metadata
description: Procedural knowledge for creating platform-ready video metadata (title, description, tags, thumbnail). Use when preparing a video for publishing.
---

# Generating Metadata

## Overview

This skill provides the procedure for creating YouTube-optimized metadata from a completed video and its source script.

## Instructions

1. **Read the script** — Load `temp/script.json` for the video's content and theme
2. **Inspect the video** — Use ffprobe to get duration, resolution, file size
3. **Craft the title** — Engaging, keyword-rich, under 100 characters
4. **Write the description** — SEO-optimized, 2-3 paragraphs with natural keywords
5. **Generate tags** — 10-15 tags, mix of broad topics and specific terms
6. **Select thumbnail timestamp** — Pick the most visually compelling scene
7. **Write metadata** — Output to `output/metadata.json`

## When to Apply

- A completed video exists in `output/`
- The quality-reviewer agent is generating platform-ready metadata
- Publishing to YouTube or similar platforms is intended

## Output Format

Write to `output/metadata.json`:

```json
{
  "title": "Engaging Title Under 100 Characters",
  "description": "First line is a hook that appears in search results.\n\nSecond paragraph expands on the content with natural keywords. Describe what the viewer will experience or learn.\n\nThird paragraph can include calls to action or related content mentions.",
  "tags": [
    "broad-topic",
    "specific-term",
    "related-concept"
  ],
  "category": "Entertainment",
  "language": "en",
  "thumbnail_timestamp": "00:00:15",
  "duration_seconds": 90,
  "resolution": "1920x1080",
  "file_size_mb": 25.4,
  "file_path": "output/video-name.mp4",
  "production_date": "2026-02-25",
  "quality_score": "pass",
  "warnings": [],
  "errors": []
}
```

## YouTube Optimization Tips

- **Title**: Front-load keywords, use emotional triggers, avoid clickbait
- **Description**: First 150 chars show in search — make them count
- **Tags**: Start with exact-match keywords, then broaden
- **Category**: Match content type (Education, Entertainment, Science & Technology, etc.)
- **Thumbnail**: Choose a scene with clear subjects, good contrast, visual interest

## References

- YouTube Creator Academy best practices
- Platform-specific character limits and requirements
