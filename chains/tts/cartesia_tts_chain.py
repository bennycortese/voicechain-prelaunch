import requests
import subprocess
from typing import AsyncGenerator, Dict, Any, Optional
from pydantic import Field
from .tts_chain import TTSChain
import aiohttp

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
                "encoding": "pcm_s16le",
                "sample_rate": 16000
            }
        }

        response = requests.post(url, headers=headers, json=payload, stream=False)

        if response.status_code == 200:
            chunks = []
            chunk_size = 1024 * 1024  # 1MB chunk size for better performance

            for chunk in response.iter_content(chunk_size=chunk_size):
               if chunk:
                   chunks.append(chunk)

            audio_data = b"".join(chunks)

            with subprocess.Popen(
                ["ffmpeg", "-f", "s16le", "-ar", "16000", "-i", "pipe:0", "-f", "wav", "pipe:1"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE
            ) as process:
                audio_content, _ = process.communicate(audio_data)

            return audio_content
        else:
            raise Exception(f"Failed to get TTS audio: {response.status_code}, {response.text}")
        
    async def generate_audio_async(self, text: str):
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
                "encoding": "pcm_s16le",
                "sample_rate": 16000
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    chunk_size = 4096

                    async for chunk in response.content.iter_chunked(n=chunk_size):
                        if chunk:
                            yield chunk
                else:
                    error_message = await response.text()
                    raise Exception(f"Failed to get TTS audio: {response.status}, {error_message}")

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        audio_content = self.generate_audio(text)
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> AsyncGenerator[Dict[str, Any], None]:
        text = inputs['text']
        async for chunk in self.generate_audio_async(text):
            yield {'audio_content': chunk}

        # text = inputs['text']
        # async for chunk in self.generate_audio_async(text):
        #     with subprocess.Popen(
        #         ["ffmpeg", "-f", "s16le", "-ar", "16000", "-i", "pipe:0", "-f", "wav", "pipe:1"],
        #         stdin=subprocess.PIPE, stdout=subprocess.PIPE
        #     ) as process:
        #         audio_content, _ = process.communicate(chunk)
        #     yield {'audio_content': audio_content}