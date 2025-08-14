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
