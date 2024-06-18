from chains.stt.whisper_stt_chain import WhisperSTTChain

if __name__ == "__main__":

    if True:
        api_key = ""
        model_id = "whisper-1"
        
        stt_chain = WhisperSTTChain(api_key=api_key, model_id=model_id)

        # Simulating audio file input for transcription
        audio_file_path = "./output.mp3"
        
        with open(audio_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        transcription = stt_chain.transcribe_audio(audio_path=audio_file_path)
        
        print("Transcription:", transcription)