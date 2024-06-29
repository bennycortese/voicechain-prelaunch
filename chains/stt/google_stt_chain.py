from google.cloud import speech_v1p1beta1 as speech
from .stt_chain import STTChain
from pydantic import Field
from typing import Dict, Any, Optional

class GoogleSTTChain(STTChain):
    credentials_path: str = Field(...)
    language_code: str = Field("en-US")

    def __init__(self, credentials_path: str, language_code: str = "en-US"):
        super().__init__()
        self.credentials_path = credentials_path
        self.language_code = language_code
        self.client = speech.SpeechClient.from_service_account_json(credentials_path)

    def transcribe_audio(self, audio_path: str) -> str:
        with open(audio_path, "rb") as audio_file:
            content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=self.language_code,
        )
        
        response = self.client.recognize(config=config, audio=audio)
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript
        
        return transcript

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        audio_bytes = inputs['audio']
        transcription = self.transcribe_audio(audio_bytes)
        return {'transcription': transcription}
