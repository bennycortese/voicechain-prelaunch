import asyncio
import subprocess
import websockets
import json
import os
import tempfile

async def send_audio(websocket, audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        await websocket.send(audio_bytes)
        print("Audio sent")  # Debugging

async def receive_messages(websocket):
    async for message in websocket:
        if isinstance(message, bytes):
            output_dir = "received_audio"
            os.makedirs(output_dir, exist_ok=True)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=output_dir) as tmp_file:
                # tmp_file.write(message)
                # tmp_file_path = tmp_file.name
                with subprocess.Popen(
                    ["ffmpeg", "-f", "s16le", "-ar", "16000", "-i", "pipe:0", "-f", "mp3", "pipe:1"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE
                ) as process:
                    audio_content, _ = process.communicate(message)
                    tmp_file.write(audio_content)
                # print(f"Received audio file: {tmp_file_path}")
        else:
            message_data = json.loads(message)
            if message_data['stage'] == 'stt':
                print("Transcription:", message_data['text'])
            elif message_data['stage'] == 'llm':
                print("LLM Response:", message_data['text'])

async def main():
    uri = "wss://137.184.123.81:5001/ws/process_audio/invite-750ee11c-6718-4eea-9b09-99a447e6633d"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")  # Debugging
        # Send the audio file
        audio_file_path = 'input_audio.mp3'  # Replace with your audio file path
        await send_audio(websocket, audio_file_path)
        
        # Receive and handle messages
        await receive_messages(websocket)

if __name__ == "__main__":
    asyncio.run(main())
