from typing import Dict, Any, Optional, List
from pydantic import Field
from langchain.chains.base import Chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from ..stt.stt_chain import STTChain
from ..tts.tts_chain import TTSChain

class SpeechToSpeechChain(Chain):
    stt_chain: STTChain = Field(...)
    llm_chain: LLMChain = Field(...)
    tts_chain: TTSChain = Field(...)

    def __init__(self, stt_chain: STTChain, llm_chain: LLMChain, tts_chain: TTSChain):
        super().__init__()
        self.stt_chain = stt_chain
        self.llm_chain = llm_chain
        self.tts_chain = tts_chain

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
        
        # LLM
        llm_output = self.llm_chain._call({'text': transcription})
        processed_text = llm_output['text']
        print("hello  ", processed_text)
        
        # TTS
        tts_output = self.tts_chain._call({'text': processed_text})
        audio_content = tts_output['audio_content']
        
        return {'audio_content': audio_content}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        # STT
        stt_output = await self.stt_chain._acall({'audio': inputs['audio']})
        transcription = stt_output['transcription']
        
        # LLM
        llm_output = await self.llm_chain._acall({'text': transcription})
        processed_text = llm_output['text']
        
        # TTS
        tts_output = await self.tts_chain._acall({'text': processed_text})
        audio_content = tts_output['audio_content']
        
        return {'audio_content': audio_content}

    @property
    def _chain_type(self) -> str:
        return "SpeechToSpeechChain"
