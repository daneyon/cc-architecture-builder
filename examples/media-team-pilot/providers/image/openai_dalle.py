"""OpenAI DALL-E 3 image generation provider."""

import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from providers.base import ImageProvider, ProviderError


class OpenAIDalleProvider(ImageProvider):
    """Generate images using OpenAI's DALL-E 3 API."""

    def __init__(self, settings: dict):
        self.settings = settings
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ProviderError(
                "openai_dalle", "OPENAI_API_KEY environment variable not set"
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
        try:
            from openai import OpenAI
        except ImportError:
            raise ProviderError(
                "openai_dalle",
                "openai package not installed. Run: pip install openai",
                retriable=False,
            )

        client = OpenAI(api_key=self.api_key)

        full_prompt = f"{style_prefix} {prompt}".strip() if style_prefix else prompt

        # DALL-E 3 supported sizes
        dalle_sizes = {"1792x1024", "1024x1792", "1024x1024"}
        if size not in dalle_sizes:
            size = "1792x1024"  # Default landscape for video

        try:
            response = client.images.generate(
                model=self.settings.get("default_model", "dall-e-3"),
                prompt=full_prompt,
                n=1,
                size=size,
                quality=quality,
                response_format="url",
            )

            image_url = response.data[0].url

            # Download the image
            import urllib.request

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(image_url, str(output_path))

            return output_path

        except Exception as e:
            raise ProviderError(
                "openai_dalle", str(e), retriable="rate" in str(e).lower()
            )
