"""OpenAI text-to-speech provider."""

import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from providers.base import TTSProvider, ProviderError


class OpenAITTSProvider(TTSProvider):
    """Generate speech audio using OpenAI's TTS API."""

    def __init__(self, settings: dict):
        self.settings = settings
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ProviderError(
                "openai_tts", "OPENAI_API_KEY environment variable not set"
            )

    def synthesize(
        self,
        text: str,
        output_path: Path,
        voice: str = "alloy",
        speed: float = 1.0,
        format: str = "mp3",
    ) -> Path:
        try:
            from openai import OpenAI
        except ImportError:
            raise ProviderError(
                "openai_tts",
                "openai package not installed. Run: pip install openai",
                retriable=False,
            )

        client = OpenAI(api_key=self.api_key)

        # OpenAI TTS voices: alloy, echo, fable, onyx, nova, shimmer
        valid_voices = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}
        if voice not in valid_voices:
            voice = "alloy"

        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=speed,
                response_format=format,
            )

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            response.stream_to_file(str(output_path))

            return output_path

        except Exception as e:
            raise ProviderError(
                "openai_tts", str(e), retriable="rate" in str(e).lower()
            )
