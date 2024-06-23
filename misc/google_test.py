from chains.tts.google_tts_chain import GoogleTTSChain
from chains.tts import tts_chain
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    
    load_dotenv()

    api_key_json_path = os.getenv("GOOGLE_CLOUD_JSON_PATH")
        
    tts_chain = GoogleTTSChain(api_key_json_path)

    text_to_speech = "I like pineapple pizza!"
        
    audio_content = tts_chain.generate_audio(text_to_speech)
        
    tts_chain.save_audio(audio_content, "google_output.mp3")
        
    print("Audio content has been saved to google_output.mp3")
