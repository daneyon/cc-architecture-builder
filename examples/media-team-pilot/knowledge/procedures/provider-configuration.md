# Provider Configuration

## Overview

The media team uses a pluggable provider system. All external API calls go through an abstraction layer defined in `providers/`. Switch between providers by editing `providers/config.json`.

## Configuring Providers

Edit `providers/config.json`:

```json
{
  "image_provider": "placeholder",
  "tts_provider": "placeholder",
  "image_settings": { ... },
  "tts_settings": { ... }
}
```

### Available Image Providers

| Value | Service | API Key Env Var |
|-------|---------|-----------------|
| `placeholder` | Test images (no API needed) | None |
| `openai_dalle` | OpenAI DALL-E 3 | `OPENAI_API_KEY` |
| `stability_ai` | Stability AI SDXL | `STABILITY_API_KEY` |

### Available TTS Providers

| Value | Service | API Key Env Var |
|-------|---------|-----------------|
| `placeholder` | Silent test audio (no API needed) | None |
| `openai_tts` | OpenAI TTS | `OPENAI_API_KEY` |
| `elevenlabs` | ElevenLabs | `ELEVENLABS_API_KEY` |

## Setting API Keys

Set environment variables (never commit keys to files):

```bash
export OPENAI_API_KEY="sk-..."
export STABILITY_API_KEY="sk-..."
export ELEVENLABS_API_KEY="..."
```

## Testing Without API Keys

Set both providers to `placeholder`:

```json
{
  "image_provider": "placeholder",
  "tts_provider": "placeholder"
}
```

This generates colored test images and near-silent audio files, allowing the full pipeline to run end-to-end without any API calls.

## Adding New Providers

1. Create a new file in `providers/image/` or `providers/tts/`
2. Implement the `ImageProvider` or `TTSProvider` base class from `providers/base.py`
3. Register the provider in `base.py`'s `load_provider()` function
4. Add the config value to this documentation
