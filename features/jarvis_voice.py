import speech_recognition as sr
import pyttsx3

class JarvisVoice:
    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id) 
        engine.say(text)
        engine.runAndWait()

    def listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1) 
            print("Listening...")
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
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