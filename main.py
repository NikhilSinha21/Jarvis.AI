'''
installed PyAudio so that it can access the audio
PyAudio is required for microphone input in speech_recognition
'''
import speech_recognition as sr # helps to recognize speech
import webbrowser #helps to access the web-browsers
import pyttsx3
import requests
from open_website import OpenWebsite
from search_things import SearchThings
from open_applications import OpenApplications
from send_message import Sendmessage
from jarvis_voice import JarvisVoice
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





def handle_open_command(command: str):
    clean_name = command[5:].strip().lower()

    if OpenApplications.is_known_app(clean_name):
        OpenApplications.open_app(command)
    else:
        OpenWebsite.process_command(command) 
    
   

if __name__ == "__main__": 
    #all texts are here
    txt_on_start = "Initializing javis"
    ai_name = "jarvis" #please name it in lowercase  
    ai_reply = "yes honey "#"On Your Command, Sir"
    #when jarvis starts  
    JarvisVoice.speak(txt_on_start)

    #listen Word jarvis to awake
    
    while True:
        

        try:
            
            word = JarvisVoice.listen()
            if not word:
                continue  # No input recognized, listen again

            if (word.lower() == ai_name):
                JarvisVoice.speak(ai_reply)
                print(ai_reply)
                
                command = JarvisVoice.listen()
                if not word:
                    continue  # No input recognized, listen again

                    #________________________________________________________
                if command.lower().startswith("search"):
                    SearchThings.process_command(command)

                elif command.lower().startswith("open"): 
                    handle_open_command(command)
                elif "message" in command.lower():
                    pass
                    Sendmessage.whatsappmessage(command) 

                else:
                    print("sorry")    
                    #________________________________________________________ 
            else:
                print("No wake word detected")


        except Exception as e:
            print(f" Unexpected error: {e}")


