from chains.tts.cartesia_tts_chain import CartesiaTTSChain
from chains.stt import stt_chain

if __name__ == "__main__":

    if True:  # Set to True to run the test
        api_key = ""
        model_id = ""
        voice_id = ""
        
        tts_chain = CartesiaTTSChain(api_key=api_key, model_id=model_id, voice_id=voice_id)

        text_to_speech = "I like pineapple pizza!"
        
        audio_content = tts_chain.generate_audio(text_to_speech)
        
        with open("input_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_content)
        
        print("Audio content has been saved to output.mp3")
