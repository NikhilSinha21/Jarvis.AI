import speech_recognition as sr
from features.file_manager import FileManager
from features.open_website import OpenWebsite
from features.search_things import SearchThings
from features.open_applications import OpenApplications
from features.send_message import Sendmessage
from features.jarvis_voice import JarvisVoice
from features.power_commands import Power
from features.system_controls import SystemControls

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
    ai_reply = "Hello, My Friend!"
    
    JarvisVoice.speak(txt_on_start)
    file_manager = FileManager()
    system_controls = SystemControls()
    
    while True:
        try:
            print("\nListening for wake word 'jarvis'...")
            word = JarvisVoice.listen()
            
            if word and ai_name in word.lower():
                JarvisVoice.speak(ai_reply)
                
                print("Listening for a command (10 second timeout)...")
                command = JarvisVoice.listen(timeout=10, phrase_time_limit=10)
                
                if command:
                    if command.lower().startswith("search"):
                        SearchThings.process_command(command)
                    elif command.lower().startswith("open"):
                        handle_open_command(command)
                    elif "message" in command.lower():
                        Sendmessage.whatsappmessage(command)
                    elif "system" in command.lower():
                        Power.power_command(command)
                    elif any(keyword in command.lower() for keyword in ["create", "delete", "rename", "move", "list", "show", "go to", "change directory", "read", "edit file", "append to file"]):
                        file_manager.process_command(command)
                    elif any(keyword in command.lower() for keyword in ["brightness", "volume", "mute", "unmute"]):
                        SystemControls.handle_system_command(command, system_controls)
                    else:
                        JarvisVoice.speak("I'm sorry, I couldn't understand that command.")
                else:
                    JarvisVoice.speak("I'll be waiting for my wake word again.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            JarvisVoice.speak("I'm sorry, an error occurred. Please try again.")
            continue

        except KeyboardInterrupt:
            print("Exiting Jarvis. Goodbye!")
            JarvisVoice.speak("Goodbye! Have a great day!")
            break