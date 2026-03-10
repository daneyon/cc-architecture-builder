"""Base provider interfaces for the pluggable media generation system."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class ImageProvider(ABC):
    """Abstract base class for image generation providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        output_path: Path,
        size: str = "1792x1024",
        quality: str = "standard",
        style_prefix: str = "",
        negative_prompt: str = "",
    ) -> Path:
        """Generate an image from a text prompt.

        Args:
            prompt: The image generation prompt.
            output_path: Where to save the generated image.
            size: Image dimensions (e.g., "1792x1024").
            quality: Quality level ("standard" or "hd").
            style_prefix: Global style to prepend to the prompt.
            negative_prompt: Elements to avoid in generation.

        Returns:
            Path to the generated image file.

        Raises:
            ProviderError: If generation fails.
        """
        ...


class TTSProvider(ABC):
    """Abstract base class for text-to-speech providers."""

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_path: Path,
        voice: str = "alloy",
        speed: float = 1.0,
        format: str = "mp3",
    ) -> Path:
        """Convert text to speech audio.

        Args:
            text: The text to speak.
            output_path: Where to save the audio file.
            voice: Voice identifier (provider-specific).
            speed: Speech rate multiplier.
            format: Output audio format.

        Returns:
            Path to the generated audio file.

        Raises:
            ProviderError: If synthesis fails.
        """
        ...


class ProviderError(Exception):
    """Raised when a provider operation fails."""

    def __init__(self, provider: str, message: str, retriable: bool = False):
        self.provider = provider
        self.retriable = retriable
        super().__init__(f"[{provider}] {message}")


def load_provider(
    provider_type: str, provider_name: str, settings: Optional[dict] = None
):
    """Load a provider by type and name.

    Args:
        provider_type: "image" or "tts"
        provider_name: Provider identifier (e.g., "openai_dalle", "placeholder")
        settings: Provider-specific settings dict.

    Returns:
        An instance of the appropriate provider.
    """
    if provider_type == "image":
        if provider_name == "placeholder":
            from providers.image.placeholder import PlaceholderImageProvider

            return PlaceholderImageProvider(settings or {})
        elif provider_name == "openai_dalle":
            from providers.image.openai_dalle import OpenAIDalleProvider

            return OpenAIDalleProvider(settings or {})
        elif provider_name == "stability_ai":
            from providers.image.stability_ai import StabilityAIProvider

            return StabilityAIProvider(settings or {})
        else:
            raise ProviderError(
                provider_name, f"Unknown image provider: {provider_name}"
            )

    elif provider_type == "tts":
        if provider_name == "placeholder":
            from providers.tts.placeholder import PlaceholderTTSProvider

            return PlaceholderTTSProvider(settings or {})
        elif provider_name == "openai_tts":
            from providers.tts.openai_tts import OpenAITTSProvider

            return OpenAITTSProvider(settings or {})
        elif provider_name == "elevenlabs":
            from providers.tts.elevenlabs import ElevenLabsTTSProvider

            return ElevenLabsTTSProvider(settings or {})
        else:
            raise ProviderError(provider_name, f"Unknown TTS provider: {provider_name}")

    else:
        raise ValueError(f"Unknown provider type: {provider_type}")
