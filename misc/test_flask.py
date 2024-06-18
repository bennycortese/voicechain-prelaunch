import requests

def send_audio_and_save_response(input_audio_path, output_audio_path, endpoint_url):
    # Read the input audio file into a byte stream
    with open(input_audio_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
    
    # Send a POST request with the audio byte stream
    files = {'file': ('input_audio.mp3', audio_bytes, 'audio/mpeg')}
    response = requests.post(endpoint_url, files=files) 
    
    # Check if the request was successful
    if response.status_code == 200 and response.headers['Content-Type'] == 'audio/mpeg':
        # Save the response byte stream to the output audio file
        with open(output_audio_path, 'wb') as output_file:
            output_file.write(response.content)
        print(f"Output audio content has been saved to {output_audio_path}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:", response.text)

# Example usage
input_audio_path = './input_audio2.mp3'
output_audio_path = './output_audio.mp3'
endpoint_url = 'http://localhost:5000/process_audio'
#endpoint_url = 'http://137.184.123.81:5000/process_audio'

send_audio_and_save_response(input_audio_path, output_audio_path, endpoint_url)
