🎤🔗 VoiceChain
✨ Building innovative applications with voice models through seamless integration ✨

Quick Install - Coming soon!

```
pip install voicechain
```

🤔 What is this?
Voice models are revolutionizing technology, enabling developers to create applications previously thought impossible. Yet, using these models in isolation often falls short of their potential. The real power emerges when they are combined with other computation or knowledge sources.

This library is designed to assist in developing these types of applications by providing:

A comprehensive collection of components you may want to combine
A flexible interface for integrating components into a single cohesive "chain"
A schema for easily saving and sharing these chains
🌟 What can I do with this?
VoiceChain was inspired by several innovative projects, including Langchain and Cartesia/ai. We've created tools to easily recreate and expand upon these ideas. Here are some examples:

Cartesia/ai
To recreate this approach, use the following code snippet or check out the example notebook.

```
from chains.tts.cartesia_tts_chain import CartesiaTTSChain
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
```

Speech Chain
To recreate this example, use the following code snippet or check out the example notebook.

```
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
```

📚 Documentation
The above examples offer a user-friendly introduction, but full API documentation can be found soon.