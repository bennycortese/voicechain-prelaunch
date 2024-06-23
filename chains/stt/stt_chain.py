from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from langchain.chains.base import Chain

# figure out a webrtc method if possible or import
class STTChain(Chain, ABC):
    """Abstract base class for Speech-to-Text chains."""
    
    @abstractmethod
    def transcribe_audio(self, audio: bytes) -> str:
        """Transcribes the given audio bytes to text."""
        pass

    @property
    def input_keys(self) -> List[str]:
        return ['audio']

    @property
    def output_keys(self) -> List[str]:
        return ['transcription']

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        audio = inputs['audio']
        transcription = self.transcribe_audio(audio)
        return {'transcription': transcription}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        # If the STT API doesn't support async natively, run the synchronous method in an executor
        from concurrent.futures import ThreadPoolExecutor
        import asyncio
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, self._call, inputs, run_manager)
        return result

    @property
    def _chain_type(self) -> str:
        return "STTChain"

