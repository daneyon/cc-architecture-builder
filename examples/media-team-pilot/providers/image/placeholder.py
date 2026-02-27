"""Placeholder image provider for testing the pipeline without API keys.

Generates colored rectangle images with scene text overlay using pure Python
(Pillow if available, or raw PPM fallback).
"""

import hashlib
import struct
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from providers.base import ImageProvider


# Scene colors — visually distinct per scene for easy identification
SCENE_COLORS = [
    (70, 130, 180),   # Steel blue
    (34, 139, 34),    # Forest green
    (178, 34, 34),    # Firebrick
    (218, 165, 32),   # Goldenrod
    (75, 0, 130),     # Indigo
    (255, 127, 80),   # Coral
    (0, 128, 128),    # Teal
    (199, 21, 133),   # Medium violet red
    (85, 107, 47),    # Dark olive green
    (100, 149, 237),  # Cornflower blue
    (210, 105, 30),   # Chocolate
    (147, 112, 219),  # Medium purple
    (60, 179, 113),   # Medium sea green
    (255, 99, 71),    # Tomato
    (106, 90, 205),   # Slate blue
    (244, 164, 96),   # Sandy brown
    (72, 209, 204),   # Medium turquoise
    (219, 112, 147),  # Pale violet red
    (143, 188, 143),  # Dark sea green
    (205, 133, 63),   # Peru
]


class PlaceholderImageProvider(ImageProvider):
    """Generates simple colored test images for pipeline testing."""

    def __init__(self, settings: dict):
        self.settings = settings

    def generate(
        self,
        prompt: str,
        output_path: Path,
        size: str = "1792x1024",
        quality: str = "standard",
        style_prefix: str = "",
        negative_prompt: str = "",
    ) -> Path:
        width, height = 1920, 1080
        if "x" in size:
            parts = size.split("x")
            width, height = int(parts[0]), int(parts[1])

        # Determine color from prompt hash for consistency
        prompt_hash = int(hashlib.md5(prompt.encode()).hexdigest(), 16)
        color = SCENE_COLORS[prompt_hash % len(SCENE_COLORS)]

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self._generate_with_pillow(prompt, output_path, width, height, color)
        except ImportError:
            self._generate_ppm_fallback(prompt, output_path, width, height, color)

        return output_path

    def _generate_with_pillow(self, prompt, output_path, width, height, color):
        """Generate image using Pillow (preferred)."""
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new("RGB", (width, height), color)
        draw = ImageDraw.Draw(img)

        # Add scene text
        text = prompt[:80] + "..." if len(prompt) > 80 else prompt
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except (OSError, IOError):
            font = ImageFont.load_default()

        # Center the text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw text with background
        padding = 20
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(0, 0, 0, 128),
        )
        draw.text((x, y), text, fill=(255, 255, 255), font=font)

        # Add "PLACEHOLDER" watermark
        try:
            wm_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        except (OSError, IOError):
            wm_font = ImageFont.load_default()
        draw.text((width // 2 - 150, height - 80), "PLACEHOLDER", fill=(255, 255, 255, 100), font=wm_font)

        img.save(str(output_path), "PNG")

    def _generate_ppm_fallback(self, prompt, output_path, width, height, color):
        """Generate image as PPM then convert, or save as PPM if no converter available."""
        # Generate raw PPM (no external deps needed)
        ppm_path = output_path.with_suffix(".ppm")

        with open(ppm_path, "wb") as f:
            header = f"P6\n{width} {height}\n255\n".encode()
            f.write(header)
            row = struct.pack("BBB", *color) * width
            for _ in range(height):
                f.write(row)

        # Try to convert to PNG using ImageMagick or ffmpeg
        import subprocess

        try:
            subprocess.run(
                ["convert", str(ppm_path), str(output_path)],
                check=True,
                capture_output=True,
            )
            ppm_path.unlink()
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-i", str(ppm_path), str(output_path)],
                    check=True,
                    capture_output=True,
                )
                ppm_path.unlink()
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fall back to PPM as the output
                ppm_path.rename(output_path)

        return output_path
