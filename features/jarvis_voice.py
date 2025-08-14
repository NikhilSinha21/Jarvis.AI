import pyttsx3
import speech_recognition as sr

class JarvisVoice:
    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # female voice
        engine.say(text)
        engine.runAndWait()

    def listen():
        speach = sr.Recognizer()
        with sr.Microphone() as source:
                print("Listening.....")
                audio = speach.listen(source,timeout=3,phrase_time_limit=3) 
                print("Recognising")  
        word = speach.recognize_google(audio,language="en-IN")
        return word    