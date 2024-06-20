from chains.tts.eleven_labs_tts_chain import ElevenLabsTTSChain
from chains.tts import tts_chain
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    
    load_dotenv()

    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    voice_id = os.getenv("ELEVEN_LABS_VOICE_ID")
<<<<<<< HEAD
=======
    print(api_key)
>>>>>>> 6ece4e0 (tts/tts_chain.py)
        
    tts_chain = ElevenLabsTTSChain(api_key=api_key, voice_id=voice_id)

    text_to_speech = "I like pineapple pizza!"
        
    audio_content = tts_chain.generate_audio(text_to_speech)
        
    tts_chain.save_audio(audio_content, "eleven_labs_output.mp3")
        
    print("Audio content has been saved to eleven_labs_output.mp3")
