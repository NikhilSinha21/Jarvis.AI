import speech_recognition as sr
from features.open_website import OpenWebsite
from features.search_things import SearchThings
from features.open_applications import OpenApplications
from features.send_message import Sendmessage
from features.jarvis_voice import JarvisVoice
from features.power_commands import Power

def handle_open_command(command: str):
    clean_name = command[5:].strip().lower()

    if OpenApplications.is_known_app(clean_name):
        OpenApplications.open_app(command)
    else:
        OpenWebsite.process_command(command) 
    
# Main execution block
if __name__ == "__main__":
    txt_on_start = "Initializing Jarvis"
    ai_name = "jarvis"
    ai_reply = "yes honey"
    
    JarvisVoice.speak(txt_on_start)

    while True:
        try:
            # First, listen for the wake word "jarvis"
            word = JarvisVoice.listen()
            if not word:
                continue

            if word.lower() == ai_name:
                JarvisVoice.speak(ai_reply)
                print(ai_reply)
                
                command = JarvisVoice.listen()
                if not word:
                    continue  # No input recognized, listen again

                if command.lower().startswith("search"): #To search websites
                    SearchThings.process_command(command)

                elif command.lower().startswith("open"): #To open applications , websites 
                    handle_open_command(command)
                elif "message" in command.lower(): # To send message on whatsapp
                    Sendmessage.whatsappmessage(command)
                elif "system" in command.lower(): #To shutdown,sleep,restart,volumn,brightness etc...
                    Power.power_command(command)         

                else:
                    print("sorry")
            else:
                # If the wake word isn't detected, do nothing and loop again
                print(f"Heard: {word}, but not the wake word.")

        except Exception as e:
            print(f"An error occurred: {e}")
            JarvisVoice.speak("I'm sorry, an error occurred. Please try again.")
            continue