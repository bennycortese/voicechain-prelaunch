from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
from .stt_chain import STTChain
from pydantic import Field
from typing import Dict, Any, Optional

class AzureSTTChain(STTChain):
    subscription_key: str = Field(...)
    region: str = Field(...)
    language_code: str = Field("en-US")

    def __init__(self, subscription_key: str, region: str, language_code: str = "en-US"):
        super().__init__()
        self.subscription_key = subscription_key
        self.region = region
        self.language_code = language_code
        self.speech_config = SpeechConfig(subscription=self.subscription_key, region=self.region)
        self.speech_config.speech_recognition_language = self.language_code

    def transcribe_audio(self, audio_path: str) -> str:
        audio_config = AudioConfig(filename=audio_path)
        recognizer = SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        result = recognizer.recognize_once()
        if result.reason == result.Reason.RecognizedSpeech:
            return result.text
        else:
            return ""

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        audio_path = inputs['audio']
        transcription = self.transcribe_audio(audio_path)
        return {'transcription': transcription}
