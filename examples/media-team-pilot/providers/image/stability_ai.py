"""Stability AI image generation provider."""

import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from providers.base import ImageProvider, ProviderError


class StabilityAIProvider(ImageProvider):
    """Generate images using Stability AI's API."""

    def __init__(self, settings: dict):
        self.settings = settings
        self.api_key = os.environ.get("STABILITY_API_KEY")
        if not self.api_key:
            raise ProviderError(
                "stability_ai", "STABILITY_API_KEY environment variable not set"
            )

    def generate(
        self,
        prompt: str,
        output_path: Path,
        size: str = "1792x1024",
        quality: str = "standard",
        style_prefix: str = "",
        negative_prompt: str = "",
    ) -> Path:
        import json
        import urllib.request

        full_prompt = f"{style_prefix} {prompt}".strip() if style_prefix else prompt

        # Parse dimensions
        width, height = 1920, 1080
        if "x" in size:
            parts = size.split("x")
            width, height = int(parts[0]), int(parts[1])

        # Stability AI expects specific aspect ratios; snap to nearest
        width = min(max(width, 512), 2048)
        height = min(max(height, 512), 2048)
        # Round to multiple of 64 (Stability requirement)
        width = (width // 64) * 64
        height = (height // 64) * 64

        api_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

        payload = json.dumps(
            {
                "text_prompts": [
                    {"text": full_prompt, "weight": 1.0},
                    *(
                        [{"text": negative_prompt, "weight": -1.0}]
                        if negative_prompt
                        else []
                    ),
                ],
                "cfg_scale": 7,
                "width": width,
                "height": height,
                "samples": 1,
                "steps": 30,
            }
        ).encode()

        req = urllib.request.Request(
            api_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read())

            import base64

            image_data = base64.b64decode(data["artifacts"][0]["base64"])

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(image_data)

            return output_path

        except Exception as e:
            raise ProviderError(
                "stability_ai", str(e), retriable="rate" in str(e).lower()
            )
