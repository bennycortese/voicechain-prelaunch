from typing import AsyncGenerator, Dict, Any, Optional
from pydantic import Field
from .tts_chain import TTSChain
from google.cloud import texttospeech
import asyncio

class GoogleTTSChain(TTSChain):
    """Concrete implementation of TTSChain for Google Text-to-Speech."""

    api_key: str = Field(...)
    client: Optional[texttospeech.TextToSpeechClient] = None

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.client = texttospeech.TextToSpeechClient.from_service_account_file(api_key)

    def generate_audio(self, text: str) -> Optional[bytes]:
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            return response.audio_content
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
        loop = asyncio.get_event_loop()
        audio_content = await loop.run_in_executor(None, self.generate_audio, text)
        if audio_content:
            yield audio_content

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        audio_content = self.generate_audio(text)
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> AsyncGenerator[Dict[str, Any], None]:
        text = inputs['text']
        async for chunk in self.generate_audio_async(text):
            yield {'audio_content': chunk}
