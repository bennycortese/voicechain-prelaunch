from chains.tts.cartesia_tts_chain import CartesiaTTSChain
from chains.stt import stt_chain
from dotenv import load_dotenv
import os

if __name__ == "__main__":

    load_dotenv()

    if True:  # Set to True to run the test
        cartesia_api_key = os.getenv("CARTESIA_API_KEY")
        model_id = "upbeat-moon"
        voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
    
        tts_chain = CartesiaTTSChain(api_key=cartesia_api_key, model_id=model_id, voice_id=voice_id)

        text_to_speech = "I like pineapple pizza!"
        
        audio_content = tts_chain.generate_audio(text_to_speech)
        
        with open("input_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_content)
        
        print("Audio content has been saved to output.mp3")
