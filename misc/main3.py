from chains.stt.whisper_stt_chain import WhisperSTTChain
from chains.tts.cartesia_tts_chain import CartesiaTTSChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from chains.sts.speech_to_speech_chain import SpeechToSpeechChain

if __name__ == "__main__":

    openai_api_key = ""
    cartesia_api_key = ""
    stt_model_id = ""
    tts_model_id = ""
    tts_voice_id = ""
    
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
