"""ElevenLabs text-to-speech provider."""

import os
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from providers.base import TTSProvider, ProviderError


# Common ElevenLabs voice name to ID mapping
VOICE_MAP = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "adam": "pNInz6obpgDQGcFmaJgB",
    "josh": "TxGEqnHWrfWFTfGW9XjX",
    "bella": "EXAVITQu4vr4xnSDxMaL",
    "alloy": "21m00Tcm4TlvDq8ikWAM",  # Map OpenAI voice name to ElevenLabs default
}


class ElevenLabsTTSProvider(TTSProvider):
    """Generate speech audio using ElevenLabs' API."""

    def __init__(self, settings: dict):
        self.settings = settings
        self.api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ProviderError(
                "elevenlabs", "ELEVENLABS_API_KEY environment variable not set"
            )

    def synthesize(
        self,
        text: str,
        output_path: Path,
        voice: str = "alloy",
        speed: float = 1.0,
        format: str = "mp3",
    ) -> Path:
        import json
        import urllib.request

        # Resolve voice name to ID
        voice_id = VOICE_MAP.get(voice.lower(), VOICE_MAP["rachel"])

        api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        payload = json.dumps(
            {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            }
        ).encode()

        req = urllib.request.Request(
            api_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "xi-api-key": self.api_key,
                "Accept": "audio/mpeg",
            },
        )

        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with urllib.request.urlopen(req) as response:
                output_path.write_bytes(response.read())

            return output_path

        except Exception as e:
            raise ProviderError(
                "elevenlabs", str(e), retriable="rate" in str(e).lower()
            )
