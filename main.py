'''
installed PyAudio so that it can access the audio
PyAudio is required for microphone input in speech_recognition
'''
import speech_recognition as sr # helps to recognize speech
import webbrowser #helps to access the web-browsers
import pyttsx3
import requests
from open_website import open_website
from search_things import search_things


'''
#________________________________________________________________________________________
engine = pyttsx3.init()

# List voices and pick female (for example, index 1)
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name} - ID: {voice.id}")

engine.setProperty('voice', voices[1].id)
#_________________________________________________________________________________________
'''
'''
def speak(text):
   # engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
   # engine.stop()
    time.sleep(0.5)

'''


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # female voice
    engine.say(text)
    engine.runAndWait()



if __name__ == "__main__": 
    #all texts are here
    txt_on_start = "Initializing javis"
    ai_name = "jarvis" #please name it in lowercase  
    ai_reply = "yes honey "#"On Your Command, Sir"
    #when jarvis starts  
    speak(txt_on_start)

    #listen Word jarvis to awake
   
while True:
    speach = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening.....")
            audio = speach.listen(source,timeout=3,phrase_time_limit=3) 
            print("Recognising")  
        word = speach.recognize_google(audio,language="en-IN")

        if (word.lower() == ai_name):
            speak(ai_reply)
            print(ai_reply)
            with sr.Microphone() as source:
                print("Listening.....")
                audio = speach.listen(source,timeout=3,phrase_time_limit=3) 
                print("Processing Command...") 
                command = speach.recognize_google(audio,language="en-IN")

                #_______________________________________________________
                if command.lower().startswith("search"):
                    search_things.process_command(command)

                #________________________________________________________    
                else: 
                    open_website.process_command(command) 

        else:
            print("No wake word detected")


    except Exception as e:
        print(f" Unexpected error: {e}")


