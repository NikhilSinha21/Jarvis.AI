'''
import speech_recognition as sr
import pyttsx3

# make jarvis voice humanoid
class JarvisVoice:
    @staticmethod
    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id) 
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def listen(timeout=10, phrase_time_limit=10):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1) 
            print("Listening...")
            
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Recognizing...")
                word = recognizer.recognize_google(audio, language="en-IN")
                return word
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start.")
                return None
'''

import pyttsx3
import whisper
import sounddevice as sd
import numpy as np
import queue
import threading

class JarvisVoice:
    @staticmethod
    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def listen(duration=7, samplerate=16000, timeout=None, phrase_time_limit=None):
        """
        Listen to microphone for `duration` seconds and return transcribed text
        using OpenAI Whisper (proper nouns like 'YouTube' preserved).
        """
        model = whisper.load_model("small")  # you can use 'base', 'medium', 'large'

        q = queue.Queue()

        def callback(indata, frames, time, status):
            if status:
                print(status)
            q.put(indata.copy())

        audio_data = []

        def threaded_record():
            with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
                for _ in range(int(duration * samplerate / 1024)):  # blocksize ~1024
                    audio_data.append(q.get())

        print("Listening...")
        t = threading.Thread(target=threaded_record)
        t.start()
        t.join()

        audio_np = np.concatenate(audio_data, axis=0).flatten().astype(np.float32)

        print("Recognizing...")
        result = model.transcribe(audio_np, fp16=False, language="en")
        command = result["text"]
        print("Recognized command:", command)
        return command
