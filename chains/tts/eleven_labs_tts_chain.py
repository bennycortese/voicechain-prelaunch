from typing import AsyncGenerator, Dict, Any, Optional
from pydantic import Field
from .tts_chain import TTSChain
from elevenlabs import save
from elevenlabs.client import ElevenLabs

class ElevenLabsTTSChain(TTSChain):
    """Concrete implementation of TTSChain for ElevenLabs Text-to-Speech."""

    api_key: str = Field(...)
    voice_id: str = Field(...)
    client: Optional[ElevenLabs] = None

    def __init__(self, api_key: str, voice_id: str):
        super().__init__()
        self.api_key = api_key
        self.voice_id = voice_id
        self.client = ElevenLabs(api_key=self.api_key)

    def generate_audio(self, text: str) -> bytes:
        audio_content = self.client.generate(
            text=text,
            voice=self.voice_id,
        )

        return audio_content

    async def generate_audio_async(self, text: str) -> AsyncGenerator[bytes, None]:
        async for audio_chunk in self.client.generate_async(
            text=text,
            voice=self.voice_id,
        ): 
            if audio_chunk:
                yield audio_chunk

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        audio_content = self.client.generate_audio(text)
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> AsyncGenerator[Dict[str, Any], None]:
        text = inputs['text']
        async for chunk in self.client.generate_audio_async(text):
            yield {'audio_content': chunk}
