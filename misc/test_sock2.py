import asyncio
import subprocess
import websockets
import json
import os
import tempfile
from pydub import AudioSegment

async def send_audio(websocket, audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
        await websocket.send(audio_bytes)
        print("Audio sent")  # Debugging

async def receive_messages(websocket, combined_audio_file_path):
    combined_audio = AudioSegment.empty()

    try:
        while True:
            async for message in websocket:
                if isinstance(message, bytes):
                    print("ran")
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir="hello") as tmp_file:
                        tmp_file.write(message)
                        tmp_file_path = tmp_file.name
                        print(tmp_file_path)

                    # Convert raw PCM data to AudioSegment
                    # audio_segment = AudioSegment.from_raw(
                    #     tmp_file_path,
                    #     sample_width=2,  # PCM s16le is 2 bytes per sample
                    #     frame_rate=16000,
                    #     channels=1
                    # )

                    # # Concatenate the new audio segment with the combined audio
                    # combined_audio += audio_segment

                    # print("Huh?")

                    # # Remove the temporary PCM file
                    # os.remove(tmp_file_path)
                else:
                    message_data = json.loads(message)
                    if message_data['stage'] == 'stt':
                        print("Transcription:", message_data['text'])
                    elif message_data['stage'] == 'llm':
                        print("LLM Response:", message_data['text'])

    except websockets.ConnectionClosed:
        print("WebSocket connection closed.")

    # Export the combined audio as an MP3 file
    combined_audio.export(combined_audio_file_path, format="mp3")
    print(f"Combined audio file saved as {combined_audio_file_path}")

async def main():
    uri = "ws://localhost:5001/ws/process_audio/invite-750ee11c-6718-4eea-9b09-99a447e6633d"
    combined_audio_file_path = 'combined_output.mp3'  # Output file path for the combined audio

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")  # Debugging

        # Send the audio file
        audio_file_path = 'input_audio.mp3'  # Replace with your audio file path
        await send_audio(websocket, audio_file_path)
        
        # Receive and handle messages
        await receive_messages(websocket, combined_audio_file_path)

if __name__ == "__main__":
    asyncio.run(main())
