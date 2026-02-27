# API Providers Reference

## Image Generation Providers

### OpenAI DALL-E 3
- **Config value**: `openai_dalle`
- **API key**: `OPENAI_API_KEY`
- **Supported sizes**: 1024x1024, 1792x1024, 1024x1792
- **Quality options**: standard, hd
- **Strengths**: Good at following complex prompts, consistent style
- **Cost**: ~$0.04/image (standard), ~$0.08/image (hd)

### Stability AI (SDXL)
- **Config value**: `stability_ai`
- **API key**: `STABILITY_API_KEY`
- **Supported sizes**: Multiples of 64, max 2048x2048
- **Strengths**: Fine-grained control, good photorealism
- **Cost**: ~$0.002-0.006/image depending on steps

### Placeholder (Test)
- **Config value**: `placeholder`
- **No API key needed**
- **Generates**: Colored rectangles with scene text overlay
- **Use for**: Pipeline testing without API costs

## TTS Providers

### OpenAI TTS
- **Config value**: `openai_tts`
- **API key**: `OPENAI_API_KEY`
- **Voices**: alloy, echo, fable, onyx, nova, shimmer
- **Models**: tts-1 (fast), tts-1-hd (quality)
- **Strengths**: Natural prosody, consistent quality
- **Cost**: ~$0.015/1K characters

### ElevenLabs
- **Config value**: `elevenlabs`
- **API key**: `ELEVENLABS_API_KEY`
- **Voices**: Large library + custom voice cloning
- **Strengths**: Most natural-sounding, voice cloning
- **Cost**: Varies by plan, ~$0.30/1K characters (starter)

### Placeholder (Test)
- **Config value**: `placeholder`
- **No API key needed**
- **Generates**: Near-silent audio files sized to match narration length
- **Use for**: Pipeline testing without API costs
