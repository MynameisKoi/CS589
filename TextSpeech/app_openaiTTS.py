import time
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import whisper
import queue
import os
import threading
import torch
import numpy as np
import re
from gtts import gTTS
import openai
import click
import sys
sys.path.append('../..')
from dotenv import load_dotenv, find_dotenv
# read local .env file
_ = load_dotenv(find_dotenv())

openai.api_key  = os.environ['OPENAI_API_KEY']

@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny", "base", "small", "medium", "large"]))
@click.option("--english", default=False, help="Whether to use the English model", is_flag=True, type=bool)
@click.option("--energy", default=300, help="Energy level for the mic to detect", type=int)
@click.option("--pause", default=0.8, help="Pause time before entry ends", type=float)
@click.option("--dynamic_energy", default=False, is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--wake_word", default="hey computer", help="Wake word to listen for", type=str)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True, type=bool)
def main(model, english, energy, pause, dynamic_energy, wake_word, verbose):
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()

    threading.Thread(target=record_audio, args=(audio_queue, energy, pause, dynamic_energy,)).start()
    threading.Thread(target=transcribe_forever, args=(audio_queue, result_queue, audio_model, english, wake_word, verbose,)).start()
    threading.Thread(target=reply, args=(result_queue,verbose,)).start()

    while True:
        print(result_queue.get())

def record_audio(audio_queue, energy, pause, dynamic_energy):
    r = sr.Recognizer()
    # print("List microphone")                      # use to debug, if microphones not found
    # print(sr.Microphone.list_microphone_names())  # then we need to change the env since it doesn't support audio
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Listening...")
        i = 0
        while True:
            audio = r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
            audio_queue.put_nowait(audio_data)
            i += 1

def transcribe_forever(audio_queue, result_queue, audio_model, english, wake_word, verbose):
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data, language='english')
        else:
            result = audio_model.transcribe(audio_data)

        predicted_text = result["text"]

        if predicted_text.strip().lower().startswith(wake_word.strip().lower()):
            pattern = re.compile(re.escape(wake_word), re.IGNORECASE)
            predicted_text = pattern.sub("", predicted_text).strip()
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            predicted_text = predicted_text.translate({ord(i): None for i in punc})
            if verbose:
                print("You said the wake word.. Processing ...")
                print("You said:" + predicted_text)

                result_queue.put_nowait(predicted_text)
        else:
            if verbose:
                print("You did not say the wake word.. Ignoring")

from pathlib import Path
from openai import OpenAI
client = OpenAI()

def reply(result_queue, verbose):
    while True:
        question = result_queue.get()
        # We use the following format for the prompt: "Q: ?\nA:"
        prompt = "Q: {}?\nA:".format(question)

        data = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100,
            n=1,
            stop=["\n"]
        )

        # We catch the exception in case there is no answer
        try:
            answer = data.choices[0].text
            print("The answer content:" + answer)
            print("Transform the answer to mp3... Result will be in speech.mp3!")
            # Replace "answer" with the actual text you want to convert to speech
            text_to_speak = answer

            # Set the output filename (modify as needed)
            speech_file_path = Path(__file__).parent / "speech.mp3"

            # Use OpenAI TTS API with desired voice and language
            response = client.audio.speech.create(
              model="tts-1",  # Adjust model if needed (check OpenAI documentation)
              voice="nova",  # Choose a voice from available options
              input=text_to_speak,
            )
            response.stream_to_file(speech_file_path)

        except Exception as e:
            choices = [
                "I'm sorry, I don't know the answer to that",
                "I'm not sure I understand",
                "I'm not sure I can answer that",
                "Please repeat the question in a different way"
            ]
            answer = choices[np.random.randint(0, len(choices))]
            print("The answer content:" + answer)
            print("Transform the answer to mp3... Result will be in speech.mp3!")
            # Replace "answer" with the actual text you want to convert to speech
            text_to_speak = answer

            # Set the output filename (modify as needed)
            speech_file_path = Path(__file__).parent / "speech.mp3"

            # Use OpenAI TTS API with desired voice and language
            response = client.audio.speech.create(
              model="tts-1",  # Adjust model if needed (check OpenAI documentation)
              voice="nova",  # Choose a voice from available options
              input=text_to_speak,
            )

            response.stream_to_file(speech_file_path)
            if verbose:
                print("Exception msg: ", e)
                print("Verbose here")

        # In both cases, we play the audio
        # audio = AudioSegment.from_file(speech_file_path)
        # play(audio)

main()
