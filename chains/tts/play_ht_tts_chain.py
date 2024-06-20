from pydantic import Field
from typing import AsyncGenerator, Dict, Any, Optional
import aiohttp
from pyht import Client, TTSOptions, Format
from .tts_chain import TTSChain

class PlayHtTTSChain(TTSChain):
    """Concrete implementation of TTSChain for PlayHT Text-to-Speech."""

    api_key: str = Field(...)
    user_id: str = Field(...)
    voice_id: str = Field("s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json", description="TTS voice id")
    client: Optional[Client] = None
    emotion: str = Field("female_happy", description="Emotion for TTS voice")

    def __init__(self, api_key: str, user_id: str, voice_id: Optional[str] = None):
        super().__init__()
        self.api_key = api_key
        self.user_id = user_id
        self.voice_id = voice_id if voice_id else "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json"
        self.client = Client(self.user_id, self.api_key)

    def generate_audio(self, text: str) -> bytes:
        # Configure TTSOptions
        options = TTSOptions(
            voice=self.voice_id,
            sample_rate=24000,
            format=Format.FORMAT_MP3,
            speed=1,
        )

        # Generate audio using the client
        audio_chunks = self.client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options)

        # Concatenate chunks into bytes
        audio_bytes = b"".join(audio_chunks)

        return audio_bytes

    async def generate_audio_async(self, text: str) -> AsyncGenerator[bytes, None]:
        options = TTSOptions(
            voice=self.voice_id,
            sample_rate=24000,
            format=Format.FORMAT_MP3,
            speed=1,
            emotion=self.emotion,
            voice_engine="PlayHT2.0"
        )

        async for chunk in self.client.tts_async(text=text, voice_engine="PlayHT2.0-turbo", options=options):
            yield chunk

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        audio_content = self.generate_audio(text)
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> AsyncGenerator[Dict[str, Any], None]:
        text = inputs['text']
        async for chunk in self.generate_audio_async(text):
            yield {'audio_content': chunk}
