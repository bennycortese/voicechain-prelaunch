from typing import AsyncGenerator, Dict, Any, Optional
from pydantic import Field
from .tts_chain import TTSChain
import asyncio
from deepgram import DeepgramClient, SpeakOptions

class DeepgramTTSChain(TTSChain):
    """Concrete implementation of TTSChain for Deepgram Text-to-Speech."""

    api_key: str = Field(...)
    client: Optional[DeepgramClient] = None

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.client = DeepgramClient(api_key)

    async def generate_audio(self, text: str) -> Optional[bytes]:
        try:
            options = SpeakOptions(
                model="aura-asteria-en",
            )
            SPEAK_OPTIONS = {"text": f"{text}"}
            filename = "deepgram.mp3"
            response = await self.client.asyncspeak.v("1").save(
                filename, SPEAK_OPTIONS, options
            )
        except Exception as e:
            print(f"Failed to generate audio: {e}")
            return None

    def save_audio(self, audio: bytes, file_path: str) -> bool:
        try:
            with open(file_path, "wb") as out:
                out.write(audio)
            return True
        except Exception as e:
            print(f"Failed to save audio: {e}")
            return False

    async def generate_audio_async(self, text: str) -> AsyncGenerator[bytes, None]:
        audio_content = await self.generate_audio(text)
        if audio_content:
            yield audio_content

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> AsyncGenerator[Dict[str, Any], None]:
        text = inputs['text']
        async for chunk in self.generate_audio_async(text):
            yield {'audio_content': chunk}

