'''
installed PyAudio so that it can access the audio
PyAudio is required for microphone input in speech_recognition
'''
import speech_recognition as sr # helps to recognize speech
import webbrowser #helps to access the web-browsers
import pyttsx3
import requests




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

def opens_url(com_in): # it check wether the link is of .com or .in
    url = webbrowser.open(f"https://{com_in}.com")
    try:
        r = requests.get(url,timeout=3)
        if r.status_code == 200:
            webbrowser.open(url)
        else:
            webbrowser.open(f"https://{com_in}.com")
    except Exception as e:
            print (f"{e}")
       
def process_command(c): 
    # open websites 
    if c.startswith("open"): # for the command which is given by the user contain "open" like open google 
        command =c[5:].strip() 
        command = command.replace(" ", "") #remove space from the text
        if "." not in command:
            #use in or com send message if i get 200 web is working
           opens_url(command)
              

        else: #if command is direct and clear
            try:
                webbrowser.open(f"https://{command}")
            except Exception as e:
                print(e)
            
    else :
         command = c.replace(" ", "")
         if "." not in command:
            #use in or com send message if i get 200 web is working
            opens_url(command)
            
         else: #if command is direct and clear
            try:
                webbrowser.open(f"https://{command}")
            except Exception as e:
                print(e)
                
if __name__ == "__main__": 
    #all texts are here
    txt_on_start = "Initializing javis"
    ai_name = "darling" #please name it in lowercase  
    ai_reply = "yes honey "#"On Your Command, Sir"
    #when jarvis starts  
    speak(txt_on_start)

    #listen Word jarvis to awake
   
while True:
    speach = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening.....")
            audio = speach.listen(source,timeout=5,phrase_time_limit=3) 
            print("Recognising")  
        word = speach.recognize_google(audio,language="en-IN")

        if (word.lower() == ai_name):
            speak(ai_reply)
            print(ai_reply)
            with sr.Microphone() as source:
                print("Listening.....")
                audio = speach.listen(source,timeout=5,phrase_time_limit=3) 
                print("Processing Command...") 
                command = speach.recognize_google(audio,language="en-IN")
                process_command(command) 

        else:
            print("No wake word detected")


    except Exception as e:
        print(f" Unexpected error: {e}")


