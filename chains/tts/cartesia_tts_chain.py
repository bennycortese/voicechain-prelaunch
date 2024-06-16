import requests
import subprocess
from typing import Dict, Any, Optional
from pydantic import Field
from .tts_chain import TTSChain

class CartesiaTTSChain(TTSChain):
    """Concrete implementation of TTSChain for Cartesia.ai Text-to-Speech."""

    api_key: str = Field(...)
    model_id: str = Field(...)
    voice_id: str = Field(...)

    def __init__(self, api_key: str, model_id: str, voice_id: str):
        super().__init__()
        self.api_key = api_key
        self.model_id = model_id
        self.voice_id = voice_id

    def generate_audio(self, text: str) -> bytes:
        url = "https://api.cartesia.ai/tts/bytes"
        headers = {
            "Cartesia-Version": "2024-06-10",
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "transcript": text,
            "model_id": self.model_id,
            "voice": {
                "mode": "id",
                "id": self.voice_id
            },
            "output_format": {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100
            }
        }

        response = requests.post(url, headers=headers, json=payload, stream=True)

        if response.status_code == 200:
            audio_data = b""
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    audio_data += chunk

            output_file = "output.mp3"
            with subprocess.Popen(
                ["ffmpeg", "-f", "f32le", "-ar", "44100", "-i", "pipe:0", "-f", "mp3", "pipe:1"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE
            ) as process:
                audio_content, _ = process.communicate(audio_data)

            return audio_content
        else:
            raise Exception(f"Failed to get TTS audio: {response.status_code}, {response.text}")

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        audio_content = self.generate_audio(text)
        return {'audio_content': audio_content}