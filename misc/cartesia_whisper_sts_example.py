from chains.stt.whisper_stt_chain import WhisperSTTChain
from chains.tts.cartesia_tts_chain import CartesiaTTSChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from chains.sts.speech_to_speech_chain import SpeechToSpeechChain
from dotenv import load_dotenv
import os

if __name__ == "__main__":

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    cartesia_api_key = os.getenv("CARTESIA_API_KEY")
    stt_model_id = "whisper-1"
    tts_model_id = "upbeat-moon"
    tts_voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
    
    # Initialize STT Chain
    stt_chain = WhisperSTTChain(api_key=openai_api_key, model_id=stt_model_id)
    
    # Initialize LLM Chain
    llm = OpenAI(api_key=openai_api_key)
    prompt = PromptTemplate(template="{text}", input_variables=["text"])
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Initialize TTS Chain
    tts_chain = CartesiaTTSChain(api_key=cartesia_api_key, model_id=tts_model_id, voice_id=tts_voice_id)
    
    # Initialize Speech-to-Speech Chain
    speech_to_speech_chain = SpeechToSpeechChain(stt_chain=stt_chain, llm_chain=llm_chain, tts_chain=tts_chain)
    
    # Simulating audio file input for transcription
    audio_file_path = "./input_audio.mp3"

    # Run the Speech-to-Speech Chain
    result = speech_to_speech_chain._call({'audio': audio_file_path})
    
    # Save the output audio content
    output_audio_path = "./output_audio.mp3"
    with open(output_audio_path, "wb") as audio_file:
        audio_file.write(result['audio_content'])
    
    print("Output audio content has been saved to", output_audio_path)
