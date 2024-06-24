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

    def generate_audio(self, text: str) -> Optional[bytes]:
        try:
            audio_content = self.client.generate(
                text=text,
                voice=self.voice_id,
            )
            if audio_content is None:
                raise ValueError("Failed to generate audio, result is None.")
            return audio_content
        except Exception as e:
            print(f"Failed to generate audio: {e}")
            return None

    def save_audio(self, audio: bytes, file_path: str) -> bool:
        try:
            save(audio, file_path)
            return True
        except Exception as e:
            print(f"Failed to save audio: {e}")
            return False

    async def generate_audio_async(self, text: str) -> AsyncGenerator[bytes, None]:
        try:
            async for audio_chunk in self.client.generate_async(
                text=text,
                voice=self.voice_id,
            ):
                if audio_chunk:
                    yield audio_chunk
        except Exception as e:
            print(f"Failed to generate audio asynchronously: {e}")

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        print(f"Generating audio for text: {text}")  # Debug logging
        audio_content = self.generate_audio(text)
        if audio_content is None:
            raise ValueError("Audio content is None.")
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        print(f"Generating audio asynchronously for text: {text}")  # Debug logging
        audio_content = b''
        async for chunk in self.generate_audio_async(text):
            audio_content += chunk
        if not audio_content:
            raise ValueError("Audio content is empty.")
        return {'audio_content': audio_content}
