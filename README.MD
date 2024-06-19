🎤🔗 VoiceChain
✨ Building innovative applications with voice models through seamless integration ✨

Quick Install

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
VoiceChain was inspired by several innovative projects, and we've created tools to easily recreate and expand upon these ideas. Here are some examples:

Cartesia/ai
To recreate this approach, use the following code snippet or check out the example notebook.

```
from chains.tts.cartesia_tts_chain import CartesiaTTSChain
from chains.stt import stt_chain

if __name__ == "__main__":

    if True:  # Set to True to run the test
        api_key = "your_api_key_here"
        model_id = "your_model_id_here"
        voice_id = "your_voice_id_here"
        
        tts_chain = CartesiaTTSChain(api_key=api_key, model_id=model_id, voice_id=voice_id)

        text_to_speech = "I like pineapple pizza!"
        
        audio_content = tts_chain.generate_audio(text_to_speech)
        
        with open("input_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_content)
        
        print("Audio content has been saved to input_audio.mp3")
```

Speech Chain
To recreate this example, use the following code snippet or check out the example notebook.

```
from chains.stt.whisper_stt_chain import WhisperSTTChain
from chains.tts.cartesia_tts_chain import CartesiaTTSChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from chains.sts.speech_to_speech_chain import SpeechToSpeechChain

if __name__ == "__main__":

    openai_api_key = "your_openai_api_key_here"
    cartesia_api_key = "your_cartesia_api_key_here"
    stt_model_id = "your_stt_model_id_here"
    tts_model_id = "your_tts_model_id_here"
    tts_voice_id = "your_tts_voice_id_here"
    
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
    
    # Simulating audio file input for transcription
    audio_file_path = "./input_audio.mp3"

    # Run the Speech-to-Speech Chain
    result = speech_to_speech_chain._call({'audio': audio_file_path})
    
    # Save the output audio content
    output_audio_path = "./output_audio.mp3"
    with open(output_audio_path, "wb") as audio_file:
        audio_file.write(result['audio_content'])
    
    print("Output audio content has been saved to", output_audio_path)
```

Interactive Voice Prompts
You can also use this for creating interactive voice prompting pipelines, as shown in the example below and this example notebook.

```
from voicechain import Prompt, VoiceAssistant, VoiceChain

template = """Question: {question}
Answer: Let's think step by step."""
prompt = Prompt(template=template, input_variables=["question"])
voice_chain = VoiceChain(prompt=prompt, voice_assistant=VoiceAssistant(clarity=0))
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
voice_chain.predict(question=question)
```

📚 Documentation
The above examples offer a user-friendly introduction, but full API documentation can be found here.