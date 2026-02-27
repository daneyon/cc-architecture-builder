#!/usr/bin/env python3
"""Generate TTS audio for each scene's narration using the configured provider.

Usage:
    python3 scripts/generate-audio.py \
        --script temp/script.json \
        --output-dir temp/assets/audio/ \
        --config providers/config.json
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from providers.base import load_provider, ProviderError


# Map narration style descriptions to provider voice names
VOICE_STYLE_MAP = {
    "calm": "alloy",
    "storytelling": "alloy",
    "reflective": "alloy",
    "energetic": "nova",
    "upbeat": "nova",
    "warm": "onyx",
    "authoritative": "onyx",
    "gentle": "shimmer",
    "friendly": "echo",
    "dramatic": "fable",
}


def resolve_voice(narration_voice_style: str, default: str = "alloy") -> str:
    """Map a style description to a provider voice name."""
    style_lower = narration_voice_style.lower()
    for keyword, voice in VOICE_STYLE_MAP.items():
        if keyword in style_lower:
            return voice
    return default


def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio from script narration")
    parser.add_argument("--script", required=True, help="Path to script.json")
    parser.add_argument("--output-dir", required=True, help="Output directory for audio files")
    parser.add_argument("--config", required=True, help="Path to provider config.json")
    parser.add_argument("--scenes", default=None, help="Comma-separated scene numbers to generate")
    args = parser.parse_args()

    # Load configs
    with open(args.script) as f:
        script_data = json.load(f)

    with open(args.config) as f:
        config = json.load(f)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize provider
    provider_name = config.get("tts_provider", "placeholder")
    tts_settings = config.get("tts_settings", {})
    print(f"Using TTS provider: {provider_name}")

    try:
        provider = load_provider("tts", provider_name, tts_settings)
    except ProviderError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine voice from script style
    narration_style = script_data.get("style", {}).get("narration_voice", "calm, storytelling")
    voice = resolve_voice(narration_style, tts_settings.get("default_voice", "alloy"))
    speed = tts_settings.get("default_speed", 1.0)
    audio_format = tts_settings.get("default_format", "mp3")
    print(f"Voice: {voice}, Speed: {speed}x")

    # Determine which scenes to generate
    scenes = script_data.get("scenes", [])
    if args.scenes:
        target_scenes = set(int(s) for s in args.scenes.split(","))
        scenes = [s for s in scenes if s["scene_number"] in target_scenes]

    # Generate audio
    errors = []
    for scene in scenes:
        scene_num = scene["scene_number"]
        narration = scene.get("narration", "")

        if not narration.strip():
            print(f"Scene {scene_num}: No narration text, skipping")
            continue

        output_path = output_dir / f"scene_{scene_num:03d}.mp3"
        print(f"Synthesizing scene {scene_num}/{len(script_data.get('scenes', []))}...")

        try:
            provider.synthesize(
                text=narration,
                output_path=output_path,
                voice=voice,
                speed=speed,
                format=audio_format,
            )
            print(f"  -> Saved: {output_path}")
        except ProviderError as e:
            error_msg = f"Scene {scene_num}: {e}"
            print(f"  -> FAILED: {error_msg}", file=sys.stderr)
            errors.append(error_msg)

        # Rate limiting delay between API calls
        if provider_name != "placeholder":
            time.sleep(0.5)

    # Write error log if any failures
    if errors:
        error_log = output_dir / "errors.log"
        error_log.write_text("\n".join(errors))
        print(f"\n{len(errors)} errors logged to {error_log}", file=sys.stderr)

    # Summary
    generated = len(list(output_dir.glob("scene_*.mp3")))
    total = len(script_data.get("scenes", []))
    print(f"\nSynthesis complete: {generated}/{total} audio files")

    if generated < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
