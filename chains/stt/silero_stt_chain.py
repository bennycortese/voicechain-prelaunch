# Silero STT with Torch
import torch
import zipfile
import torchaudio
from glob import glob
from typing import Dict, Any, Optional, List
from langchain.chains.base import Chain
from abc import ABC, abstractmethod

device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU

model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en',  # also available 'de', 'es'
                                       device=device)
(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils  # see function signature for details

class SileroSTTChain(Chain, ABC):
    """Concrete implementation of Speech-to-Text chain using Silero STT."""

    @abstractmethod
    def transcribe_audio(self, audio: str) -> str:
        """Transcribes the given audio file path to text."""
        test_files = [audio]
        batches = split_into_batches(test_files, batch_size=1)
        input_data = prepare_model_input(read_batch(batches[0]), device=device)
        output = model(input_data)
        transcriptions = [decoder(example.cpu()) for example in output]
        return transcriptions[0]

    @property
    def input_keys(self) -> List[str]:
        return ['audio']

    @property
    def output_keys(self) -> List[str]:
        return ['transcription']

    def _call(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        audio = inputs['audio']
        transcription = self.transcribe_audio(audio)
        return {'transcription': transcription}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional = None) -> Dict[str, Any]:
        # If the STT API doesn't support async natively, run the synchronous method in an executor
        from concurrent.futures import ThreadPoolExecutor
        import asyncio
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, self._call, inputs, run_manager)
        return result

    @property
    def _chain_type(self) -> str:
        return "STTChain"

if __name__ == "__main__":
    # Example usage
    stt_chain = SileroSTTChain()

    # Download sample audio file
    torch.hub.download_url_to_file('https://opus-codec.org/static/examples/samples/speech_orig.wav',
                                   dst='speech_orig.wav', progress=True)
    audio_file_path = 'speech_orig.wav'

    # Run the STT chain
    inputs = {'audio': audio_file_path}
    result = stt_chain._call(inputs)
    print("Transcription:", result['transcription'])

    # For async usage
    # result = asyncio.run(stt_chain._acall(inputs))
    # print("Async Transcription:", result['transcription'])
