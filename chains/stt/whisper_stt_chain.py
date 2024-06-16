from openai import OpenAI
from .stt_chain import STTChain
from pydantic import Field
from typing import Dict, Any, Optional

class WhisperSTTChain(STTChain):
    api_key: str = Field(...)
    model_id: str = Field(...)
    client: OpenAI = None

    def __init__(self, api_key: str, model_id: str):
        super().__init__()
        self.api_key = api_key
        self.model_id = model_id
        self.client = OpenAI(api_key=self.api_key)

    def transcribe_audio(self, audio_path: str) -> str:
        audio_file = open(audio_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model=self.model_id, 
            file=audio_file
        )
        return transcription.text
    
    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        audio_bytes = inputs['audio']
        transcription = self.transcribe_audio(audio_bytes)
        return {'transcription': transcription}
