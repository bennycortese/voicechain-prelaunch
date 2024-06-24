from chains.stt.whisper_stt_chain import WhisperSTTChain
from chains.tts.eleven_labs_tts_chain import ElevenLabsTTSChain
from chains.sts.speech_to_speech_chain import SpeechToSpeechChain
from chains.ttt.cohere_wikipedia_ttt_chain import CohereWikipediaTTTChain
from dotenv import load_dotenv
import os
import asyncio

if __name__ == "__main__":

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
    eleven_labs_voice_id = os.getenv("ELEVEN_LABS_VOICE_ID")
    cohere_api_key = os.getenv("COHERE_API_KEY")
    stt_model_id = "whisper-1"
    
    # Initialize STT Chain
    stt_chain = WhisperSTTChain(api_key=openai_api_key, model_id=stt_model_id)
    
    # Initialize Cohere agent for Wikipedia lookups
    cohere_chain = CohereWikipediaTTTChain(api_key=cohere_api_key)

    # Initialize TTS Chain
    tts_chain = ElevenLabsTTSChain(api_key=eleven_labs_api_key, voice_id=eleven_labs_voice_id)
    
    # Initialize Speech-to-Speech Chain
    speech_to_speech_chain = SpeechToSpeechChain(
        stt_chain=stt_chain,
        llm_chain=cohere_chain,
        tts_chain=tts_chain
    )
    
    # Simulating audio file input for transcription
    audio_file_path = "./input_audio.mp3"

    # Run the Speech-to-Speech Chain
    result = speech_to_speech_chain._call({'audio': audio_file_path})
    
    # Save the output audio content
    output_audio_path = "./output_audio.mp3"
    speech_to_speech_chain.tts_chain.save_audio(result['audio_content'], output_audio_path)
    
    print("Output audio content has been saved to", output_audio_path)
