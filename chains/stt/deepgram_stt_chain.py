from typing import Dict, Any, Optional, List
from pydantic import Field
from .stt_chain import STTChain
from deepgram import DeepgramClient

class DeepgramSTTChain(STTChain):
    """Concrete implementation of STTChain for Deepgram Speech-to-Text."""

    api_key: str = Field(...)
    client: Optional[DeepgramClient] = None

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.client = DeepgramClient(api_key)

    def transcribe_audio(self, audio: bytes) -> str:
        try:
            response = self.client.transcription.pre_recorded(
                audio, {'punctuate': True, 'language': 'en-US'}
            )
            transcription = response['results']['channels'][0]['alternatives'][0]['transcript']
            return transcription
        except Exception as e:
            print(f"Failed to transcribe audio: {e}")
            return ""

    async def transcribe_audio_async(self, audio: bytes) -> str:
        try:
            response = await self.client.transcription.pre_recorded_async(
                audio, {'punctuate': True, 'language': 'en-US'}
            )
            transcription = response['results']['channels'][0]['alternatives'][0]['transcript']
            return transcription
        except Exception as e:
            print(f"Failed to transcribe audio: {e}")
            return ""

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        audio = inputs['audio']
        transcription = await self.transcribe_audio_async(audio)
        return {'transcription': transcription}
