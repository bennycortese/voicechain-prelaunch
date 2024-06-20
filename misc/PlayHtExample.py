from chains.tts.play_ht_tts_chain import PlayHtTTSChain
from chains.tts import tts_chain
from dotenv import load_dotenv
import os

if __name__ == "__main__":
         
        api_key = os.getenv("PLAY_HT_API_KEY")
        user_id = os.getenv("PLAY_HT_USER_ID")
        
        tts_chain = PlayHtTTSChain(api_key=api_key, user_id=user_id)

        text_to_speech = "I like pineapple pizza!"
        
        audio_content = tts_chain.generate_audio(text_to_speech)
        
        with open("playht_test_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_content)

        print("Audio content has been saved to playht_test_audio.mp3")
