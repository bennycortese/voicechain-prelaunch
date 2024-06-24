import asyncio
from typing import Dict, Any, Optional, List, Callable, Union
from pydantic import Field
from langchain.chains.base import Chain
from langchain.chains import LLMChain
from ..stt.stt_chain import STTChain
from ..tts.tts_chain import TTSChain

class SpeechToSpeechChain(Chain):
    stt_chain: STTChain = Field(...)
    llm_chain: LLMChain = Field(...)
    tts_chain: TTSChain = Field(...)
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    callback: Optional[Callable[[str, Union[str, bytes]], None]] = None

    def __init__(self, stt_chain: STTChain, llm_chain: LLMChain, tts_chain: TTSChain, callback: Optional[Callable[[str, Union[str, bytes]], None]] = None):
        super().__init__()
        self.stt_chain = stt_chain
        self.llm_chain = llm_chain
        self.tts_chain = tts_chain
        self.conversation_history = []
        self.callback = callback

    @property
    def input_keys(self) -> List[str]:
        return ['audio']

    @property
    def output_keys(self) -> List[str]:
        return ['audio_content']

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        # STT
        stt_output = self.stt_chain._call({'audio': inputs['audio']})
        transcription = stt_output['transcription']
        self._invoke_callback('stt', transcription)
        
        # Update conversation history
        self.conversation_history.append({'role': 'user', 'text': transcription})
        
        # Prepare conversation context for LLM
        context = "\n".join([f"{entry['role']}: {entry['text']}" for entry in self.conversation_history])
        prompt = f"The following is a conversation between a user and an AI assistant. The assistant should maintain context and respond accordingly.\n\n{context}\n\nAI assistant:"
        
        # LLM
        llm_output = self.llm_chain._call({'text': prompt})
        processed_text = llm_output['text']
        self._invoke_callback('llm', processed_text)
        
        # Update conversation history
        self.conversation_history.append({'role': 'system', 'text': processed_text})
        
        # TTS
        tts_output = self.tts_chain._call({'text': processed_text})
        audio_content = tts_output['audio_content']
        if audio_content is None:
            print("TTS output is None")  # Debug logging
            raise ValueError("Audio content is None.")
        self._invoke_callback('tts', audio_content)
        
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        # STT
        stt_output = await self.stt_chain._acall({'audio': inputs['audio']})
        transcription = stt_output['transcription']
        await self._invoke_callback_async('stt', transcription)
        
        # Update conversation history
        self.conversation_history.append({'role': 'user', 'text': transcription})
        
        # Prepare conversation context for LLM
        context = "\n".join([f"{entry['role']}: {entry['text']}" for entry in self.conversation_history])
        prompt = f"The following is a conversation between a user and an AI assistant. The assistant should maintain context and respond accordingly. It should also be concise.\n\n{context}\n\nAI assistant:"
        
        # LLM
        llm_output = await self.llm_chain._acall({'text': prompt})
        processed_text = llm_output['text']
        await self._invoke_callback_async('llm', processed_text)
        
        # Update conversation history
        self.conversation_history.append({'role': 'system', 'text': processed_text})
        
        # TTS
        audio_content = b''
        async for tts_output in self.tts_chain._acall({'text': processed_text}):
            audio_content += tts_output['audio_content']
            await self._invoke_callback_async('tts', tts_output['audio_content'])
        
        if not audio_content:
            print("TTS async output is empty")  # Debug logging
            raise ValueError("Audio content is empty.")
        
        return {'audio_content': audio_content}

    @property
    def _chain_type(self) -> str:
        return "SpeechToSpeechChain"
    
    def clear_conversation_history(self):
        self.conversation_history = []

    def _invoke_callback(self, stage: str, data: Any):
        if self.callback:
            self.callback(stage, data)

    async def _invoke_callback_async(self, stage: str, data: Any):
        if self.callback:
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback(stage, data)
            else:
                self.callback(stage, data)
