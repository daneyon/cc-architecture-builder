#!/usr/bin/env python3
"""Generate images for each scene using the configured provider.

Usage:
    python3 scripts/generate-images.py \
        --prompts temp/image-prompts.json \
        --output-dir temp/assets/images/ \
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


def main():
    parser = argparse.ArgumentParser(description="Generate images from scene prompts")
    parser.add_argument("--prompts", required=True, help="Path to image-prompts.json")
    parser.add_argument("--output-dir", required=True, help="Output directory for images")
    parser.add_argument("--config", required=True, help="Path to provider config.json")
    parser.add_argument("--scenes", default=None, help="Comma-separated scene numbers to generate (e.g., 3,5,7)")
    args = parser.parse_args()

    # Load configs
    for filepath in [args.prompts, args.config]:
        if not Path(filepath).exists():
            print(f"ERROR: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)

    with open(args.prompts) as f:
        prompts_data = json.load(f)

    with open(args.config) as f:
        config = json.load(f)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize provider
    provider_name = config.get("image_provider", "placeholder")
    image_settings = config.get("image_settings", {})
    print(f"Using image provider: {provider_name}")

    try:
        provider = load_provider("image", provider_name, image_settings)
    except ProviderError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine which scenes to generate
    scenes = prompts_data.get("scenes", [])
    if args.scenes:
        target_scenes = set(int(s) for s in args.scenes.split(","))
        scenes = [s for s in scenes if s["scene_number"] in target_scenes]

    global_style = prompts_data.get("global_style", "")
    negative_prompt = prompts_data.get("negative_prompt", "")
    size = image_settings.get("default_size", "1792x1024")

    # Generate images
    errors = []
    for scene in scenes:
        scene_num = scene["scene_number"]
        output_path = output_dir / f"scene_{scene_num:03d}.png"

        print(f"Generating scene {scene_num}/{len(prompts_data.get('scenes', []))}...")

        try:
            provider.generate(
                prompt=scene["prompt"],
                output_path=output_path,
                size=size,
                style_prefix=global_style,
                negative_prompt=negative_prompt,
            )
            print(f"  -> Saved: {output_path}")
        except ProviderError as e:
            error_msg = f"Scene {scene_num}: {e}"
            print(f"  -> FAILED: {error_msg}", file=sys.stderr)
            errors.append(error_msg)

        # Rate limiting delay between API calls
        if provider_name != "placeholder":
            time.sleep(1.5)

    # Write error log if any failures
    if errors:
        error_log = output_dir / "errors.log"
        error_log.write_text("\n".join(errors))
        print(f"\n{len(errors)} errors logged to {error_log}", file=sys.stderr)

    # Summary
    generated_count = len(scenes) - len(errors)
    target_count = len(scenes)
    total = len(prompts_data.get("scenes", []))
    print(f"\nGeneration complete: {generated_count}/{target_count} targeted scenes ({total} total in script)")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
