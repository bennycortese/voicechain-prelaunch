from azure_stt_chain import AzureSTTChain
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()

    subscription_key = os.getenv("AZURE_SUBSCRIPTION_KEY")
    region = os.getenv("AZURE_REGION")
    
    audio_path = "azure_output.wav"
    
    stt_chain = AzureSTTChain(subscription_key=subscription_key, region=region)
    
    inputs = {'audio': audio_path}
    result = stt_chain._call(inputs)
    
    print("Transcription:", result['transcription'])
