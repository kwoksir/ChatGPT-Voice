import openai
import pyttsx3
#python -m pip install pypiwin32 pyaudio pyttsx3

import speech_recognition as sr
#python -m pip install SpeechRecognition==3.8.1

import os
import azure.cognitiveservices.speech as speechsdk
#python -m pip install azure-cognitiveservices-speech

openai.api_key = ""
SPEECH_KEY = ""
SPEECH_REGION = "eastus"
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='en-GB-RyanNeural'

#https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=stt-tts#prebuilt-neural-voices
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
engine = pyttsx3.init()
r= sr.Recognizer()
mic = sr.Microphone(device_index=0)

while True:
    with mic as source:
        print("\nlistening... speak clearly into mic.")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening.\n")
    try:
        user_input = r.recognize_google(audio,show_all=False)
    except:
        continue
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
        {"role": "user", "content": user_input},
    ])

    response_str = response["choices"][0]["message"]['content']
    print(response_str)
    speech_synthesis_result = speech_synthesizer.speak_text_async(response_str).get()
    engine.runAndWait()
