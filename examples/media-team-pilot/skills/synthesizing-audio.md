---
name: synthesizing-audio
description: Procedural knowledge for generating text-to-speech audio via the pluggable provider system. Use when the media-producer agent needs to create narration audio from script text.
---

# Synthesizing Audio

## Overview

This skill provides the procedure for generating text-to-speech narration audio using the configured TTS provider. Each scene's narration text is converted to an individual audio file.

## Instructions

1. **Read the provider config** — Check `providers/config.json` for the active `tts_provider`
2. **Read the script** — Load `temp/script.json` for scene narration text and voice style
3. **Ensure output directory exists** — Create `temp/assets/audio/` if needed
4. **Run the generation script**:
   ```bash
   python3 scripts/generate-audio.py \
     --script temp/script.json \
     --output-dir temp/assets/audio/ \
     --config providers/config.json
   ```
5. **Verify outputs** — Check that one .mp3 file exists per scene in `temp/assets/audio/`

## When to Apply

- The media-producer agent is generating audio assets for a video
- A script with narration text exists at `temp/script.json`
- The provider config file exists with a valid TTS provider selection

## Output Format

Generated files follow the naming convention:
```
temp/assets/audio/scene_001.mp3
temp/assets/audio/scene_002.mp3
...
temp/assets/audio/scene_NNN.mp3
```

## Provider Options

| Provider | Config Value | Requires |
|----------|-------------|----------|
| OpenAI TTS | `openai_tts` | `OPENAI_API_KEY` env var |
| ElevenLabs | `elevenlabs` | `ELEVENLABS_API_KEY` env var |
| Google TTS | `google_tts` | `GOOGLE_APPLICATION_CREDENTIALS` env var |
| Placeholder (test) | `placeholder` | Nothing — generates silent audio files |

## Voice Configuration

The script reads voice preferences from the script's `style.narration_voice` field and maps to provider-specific voice IDs:

| Style | OpenAI | ElevenLabs |
|-------|--------|------------|
| calm, storytelling | `alloy` | `Rachel` |
| energetic, upbeat | `nova` | `Josh` |
| warm, authoritative | `onyx` | `Adam` |

## Troubleshooting

- **API key missing**: Check environment variables match provider requirements
- **Rate limiting**: The script includes built-in delays between API calls
- **Failed generation**: Check `temp/assets/audio/errors.log` for details
- **Audio quality issues**: Try a different voice or adjust speech rate in config
