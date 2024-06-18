import asyncio
import websockets
import json
import os
import tempfile
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from chains.stt import WhisperSTTChain
from chains.tts import CartesiaTTSChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from chains.sts.speech_to_speech_chain import SpeechToSpeechChain
from io import BytesIO
from typing import Dict, Any, Optional, List, Callable

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

openai_api_key = ""
cartesia_api_key = ""
stt_model_id = ""
tts_model_id = ""
tts_voice_id = ""

# Initialize STT Chain
stt_chain = WhisperSTTChain(api_key=openai_api_key, model_id=stt_model_id)

# Initialize LLM Chain
llm = OpenAI(api_key=openai_api_key)
prompt = PromptTemplate(template="{text}", input_variables=["text"])
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Initialize TTS Chain
tts_chain = CartesiaTTSChain(api_key=cartesia_api_key, model_id=tts_model_id, voice_id=tts_voice_id)

with open('invite_codes.json', 'r') as file:
    invite_codes = json.load(file)

@app.websocket("/ws/process_audio/{invite_code}")
async def websocket_endpoint(websocket: WebSocket, invite_code: str):
    await websocket.accept()

    if invite_code not in invite_codes:
        raise HTTPException("You don't have a proper invite code to use our product", status_code=401)
    else:
        #if(invite_codes[invite_code] >= 100): 
        #    raise HTTPException("Too many requests from the same user", status_code=429)

        invite_codes[invite_code] += 1

        with open('invite_codes.json', 'w') as file:
            json.dump(invite_codes, file)

    def callback(stage: str, data: Any):
        if stage in ['stt', 'llm']:
            asyncio.create_task(websocket.send_json({"stage": stage, "text": data}))
        elif stage == 'tts':
            asyncio.create_task(websocket.send_bytes(data))

    # Initialize Speech-to-Speech Chain with the callback
    speech_to_speech_chain = SpeechToSpeechChain(stt_chain=stt_chain, llm_chain=llm_chain, tts_chain=tts_chain, callback=callback)

    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            # if not audio_bytes:
            #     await websocket.close(code=1000)
            #     break

            # Create a temporary file to save the byte stream
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name

            try:
                # Run the Speech-to-Speech Chain with the temporary file path
                result = await speech_to_speech_chain._acall({'audio': tmp_file_path})

                invite_codes[invite_code] += 1
                #if(invite_codes[invite_code] >= 100): 
                #    raise HTTPException("Too many requests from the same user", status_code=429)
        
                output_audio_bytes = result['audio_content']
            finally:
                # Ensure the temporary file is deleted
                os.remove(tmp_file_path)

    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5001)