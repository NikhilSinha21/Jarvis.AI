

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
