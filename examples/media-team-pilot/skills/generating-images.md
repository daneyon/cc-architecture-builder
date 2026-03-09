---
name: generating-images
description: Procedural knowledge for generating images via the pluggable provider system. Use when the media-producer agent needs to create visual assets from prompts.
---

# Generating Images

## Overview

This skill provides the procedure for generating images using the configured provider. It wraps the provider abstraction layer so the calling agent doesn't need to know which specific API is active.

## Instructions

1. **Read the provider config** — Check `providers/config.json` for the active `image_provider`
2. **Read the image prompts** — Load `temp/image-prompts.json` for scene prompts and global style
3. **Ensure output directory exists** — Create `temp/assets/images/` if needed
4. **Run the generation script**:
   ```bash
   python3 scripts/generate-images.py \
     --prompts temp/image-prompts.json \
     --output-dir temp/assets/images/ \
     --config providers/config.json
   ```
5. **Verify outputs** — Check that one .png file exists per scene in `temp/assets/images/`

## When to Apply

- The media-producer agent is generating visual assets for a video
- Image prompts have already been created by the visual-designer agent
- The provider config file exists with a valid image provider selection

## Output Format

Generated files follow the naming convention:
```
temp/assets/images/scene_001.png
temp/assets/images/scene_002.png
...
temp/assets/images/scene_NNN.png
```

## Provider Options

| Provider | Config Value | Requires |
|----------|-------------|----------|
| OpenAI DALL-E 3 | `openai_dalle` | `OPENAI_API_KEY` env var |
| Stability AI | `stability_ai` | `STABILITY_API_KEY` env var |
| Placeholder (test) | `placeholder` | Nothing — generates colored test images |

## Troubleshooting

- **API key missing**: Check environment variables match provider requirements
- **Rate limiting**: The script includes built-in delays between API calls
- **Failed generation**: Check `temp/assets/images/errors.log` for details
- **Wrong image count**: Re-run for specific scenes by passing `--scenes 3,5,7`
