from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from chains.stt import WhisperSTTChain
from chains.tts import CartesiaTTSChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from chains.sts.speech_to_speech_chain import SpeechToSpeechChain
from io import BytesIO
import tempfile
import os

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

# Initialize Speech-to-Speech Chain
speech_to_speech_chain = SpeechToSpeechChain(stt_chain=stt_chain, llm_chain=llm_chain, tts_chain=tts_chain)

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No audio file provided")

    audio_bytes = await file.read()

    # Create a temporary file to save the byte stream
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file_path = tmp_file.name

    try:
        # Run the Speech-to-Speech Chain with the temporary file path
        result = speech_to_speech_chain._call({'audio': tmp_file_path})
        output_audio_bytes = result['audio_content']
    finally:
        # Ensure the temporary file is deleted
        os.remove(tmp_file_path)

    # Create a BytesIO object for the output byte stream
    output_audio_stream = BytesIO(output_audio_bytes)
    output_audio_stream.seek(0)
    
    return StreamingResponse(output_audio_stream, media_type='audio/mpeg', headers={'Content-Disposition': 'attachment; filename=output_audio.mp3'})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
