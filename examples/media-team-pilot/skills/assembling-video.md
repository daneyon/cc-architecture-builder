---
name: assembling-video
description: Procedural knowledge for combining images and audio into a final .mp4 video using ffmpeg. Use when the video-assembler agent needs to produce the final video.
---

# Assembling Video

## Overview

This skill provides the procedure for combining scene images and narration audio into a final .mp4 slideshow video using ffmpeg, with Ken Burns effects and crossfade transitions.

## Instructions

1. **Read the script** — Load `temp/script.json` for scene timing and transitions
2. **Verify assets** — Confirm matching image and audio files exist in `temp/assets/`
3. **Run the assembly script**:
   ```bash
   bash scripts/assemble-video.sh \
     --script temp/script.json \
     --images temp/assets/images/ \
     --audio temp/assets/audio/ \
     --output output/
   ```
4. **Verify the output** — Check the .mp4 exists and has audio+video streams:
   ```bash
   ffprobe -v quiet -print_format json -show_streams output/*.mp4
   ```

## When to Apply

- The video-assembler agent has confirmed all image and audio assets are ready
- Scene timing information is available in `temp/script.json`
- ffmpeg is available in PATH

## Assembly Pipeline

The script performs these steps internally:

```
For each scene:
  1. Scale image to 1920x1080
  2. Apply Ken Burns effect (slow zoom over scene duration)
  3. Create video segment from image
  4. Attach scene audio to video segment

Then:
  5. Concatenate all scene segments
  6. Apply crossfade transitions between scenes
  7. Encode final output (H.264 + AAC)
```

## Output Specifications

| Property | Value |
|----------|-------|
| Resolution | 1920x1080 |
| Framerate | 30 fps |
| Video codec | H.264 (libx264) |
| Audio codec | AAC |
| Container | .mp4 |
| Quality | CRF 23 (good balance) |

## Common ffmpeg Patterns

### Scale and pad image to 1920x1080
```bash
ffmpeg -i input.png -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" output.png
```

### Ken Burns (zoom in)
```bash
ffmpeg -loop 1 -i scene.png -t 10 -vf "zoompan=z='min(zoom+0.0015,1.5)':d=300:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30" -c:v libx264 -pix_fmt yuv420p scene.mp4
```

### Combine video + audio
```bash
ffmpeg -i scene.mp4 -i scene.mp3 -c:v copy -c:a aac -shortest scene_final.mp4
```

### Concatenate scenes
```bash
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```

## Troubleshooting

- **ffmpeg not found**: Install via `apt install ffmpeg` or `brew install ffmpeg`
- **Black frames**: Image wasn't properly scaled — check aspect ratio handling
- **Audio desync**: Verify scene durations match audio file lengths
- **Large file size**: Increase CRF value (e.g., 28) or reduce resolution
