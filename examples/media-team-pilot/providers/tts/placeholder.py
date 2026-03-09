"""Placeholder TTS provider for testing the pipeline without API keys.

Generates silent audio files of appropriate duration based on narration text length.
Uses ffmpeg to create the silence, or falls back to a raw WAV file.
"""

import subprocess
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from providers.base import TTSProvider


# Average speech rate: ~150 words per minute = 2.5 words per second
WORDS_PER_SECOND = 2.5


class PlaceholderTTSProvider(TTSProvider):
    """Generates silent audio files sized to match narration text length."""

    def __init__(self, settings: dict):
        self.settings = settings

    def synthesize(
        self,
        text: str,
        output_path: Path,
        voice: str = "alloy",
        speed: float = 1.0,
        format: str = "mp3",
    ) -> Path:
        # Estimate duration from word count
        word_count = len(text.split())
        duration = max(2.0, word_count / (WORDS_PER_SECOND * speed))

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self._generate_with_ffmpeg(output_path, duration, format)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self._generate_wav_fallback(output_path, duration)

        return output_path

    def _generate_with_ffmpeg(self, output_path, duration, format):
        """Generate silent audio using ffmpeg."""
        # Generate a sine wave at very low volume (quasi-silent but valid audio)
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency=440:duration={duration:.1f}",
            "-af", "volume=0.01",
            "-ar", "44100",
            "-ac", "1",
        ]

        if format == "mp3":
            cmd.extend(["-codec:a", "libmp3lame", "-b:a", "128k"])
        else:
            cmd.extend(["-codec:a", "aac", "-b:a", "128k"])

        cmd.append(str(output_path))
        subprocess.run(cmd, check=True, capture_output=True)

    def _generate_wav_fallback(self, output_path, duration):
        """Generate a minimal WAV file without external dependencies."""
        import struct
        import wave

        sample_rate = 44100
        num_frames = int(sample_rate * duration)

        wav_path = output_path.with_suffix(".wav")
        with wave.open(str(wav_path), "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            # Write near-silent frames
            silence = struct.pack("<h", 1) * num_frames
            wav_file.writeframes(silence)

        # If output was supposed to be mp3, keep as wav (ffmpeg not available)
        if output_path.suffix != ".wav":
            wav_path.rename(output_path.with_suffix(".wav"))
