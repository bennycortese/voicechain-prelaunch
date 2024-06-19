from chains.tts.eleven_labs_tts_chain import ElevenLabsTTSChain
from chains.tts import tts_chain
from elevenlabs import save

if __name__ == "__main__":

    if True:  # Set to True to run the test
        api_key = ""
        voice_id = ""
        
        tts_chain = ElevenLabsTTSChain(api_key=api_key, voice_id=voice_id)

        text_to_speech = "I like pineapple pizza!"
        
        audio_content = tts_chain.generate_audio(text_to_speech)
        
        save(audio_content, "output.mp3") # Should likely introduce a default save abstraction so we can override it with this for eleven_labs
        
        print("Audio content has been saved to output.mp3")
