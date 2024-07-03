from deepgram import Deepgram
from deepgram_stt_chain import DeepgramSTTChain
from dotenv import load_dotenv
import os
import asyncio

async def main():
    load_dotenv()

    api_key = os.getenv("DEEPGRAM_API_KEY")
    
    # Read audio file
    with open("path/to/your/audio/file.wav", "rb") as audio_file:
        audio_content = audio_file.read()
    
    stt_chain = DeepgramSTTChain(api_key=api_key)
    
    inputs = {'audio': audio_content}
    result = await stt_chain._acall(inputs)
    
    print("Transcription:", result['transcription'])

if __name__ == "__main__":
    asyncio.run(main())
