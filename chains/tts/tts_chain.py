from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from langchain.chains.base import Chain

class TTSChain(Chain, ABC):
    """Abstract base class for Text-to-Speech chains."""
    
    @abstractmethod
    def generate_audio(self, text: str) -> bytes:
        """Generates audio bytes from the given text."""
        pass

    @property
    def input_keys(self) -> List[str]:
        return ['text']

    @property
    def output_keys(self) -> List[str]:
        return ['audio_content']

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        text = inputs['text']
        audio_content = self.generate_audio(text)
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        # If the TTS API doesn't support async natively, run the synchronous method in an executor
        from concurrent.futures import ThreadPoolExecutor
        import asyncio
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, self._call, inputs, run_manager)
        return result

    @property
    def _chain_type(self) -> str:
        return "TTSChain"
