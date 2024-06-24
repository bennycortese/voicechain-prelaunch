from chains.tts.deepgram_tts_chain import DeepgramTTSChain
from chains.tts import tts_chain
from dotenv import load_dotenv
import os
import asyncio

if __name__ == "__main__":
    
    load_dotenv()

    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
        
    tts_chain = DeepgramTTSChain(deepgram_api_key)

    text_to_speech = "I like pineapple pizza!"

    async def main():
        audio_content = await tts_chain.generate_audio(text_to_speech)
        if audio_content:
            tts_chain.save_audio(audio_content, "deepgram_output.mp3")
            print("Audio content has been saved to deepgram_output.mp3")

    asyncio.run(main())
