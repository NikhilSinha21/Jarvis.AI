from open_applications import OpenApplications
import pyautogui
import speech_recognition as sr
import time
from jarvis_voice import JarvisVoice

class Sendmessage:
    def confirmation(name,message):
        # Step 1: Focus input and type message but DON'T send yet
        pyautogui.write(message)
        
        # Step 2: Ask for confirmation
        JarvisVoice.speak(f"Are you sure you want to send this message to {name}? Please say please if yes.")
        
        time.sleep(2)  # wait briefly for user to prepare to answer

        try:
            answer = JarvisVoice.listen()
        except Exception:
            JarvisVoice.speak("Sorry, I didn't catch that. Message will not be sent.")
            pyautogui.hotkey('ctrl', 'a')  # select all typed text
            pyautogui.press('backspace')   # clear message
            return
        
        # Step 3: Send or cancel based on answer
        if 'please' in answer.lower():
            pyautogui.press("enter")  # send message
            JarvisVoice.speak("Message sent.")
        else:
            pyautogui.hotkey('ctrl', 'a')  # select all typed text
            pyautogui.press('backspace')   # clear message
            JarvisVoice.speak("Message cancelled.")

    def find_name(name,message):
        pyautogui.write(name)
        time.sleep(3)  # wait for search results to appear
        pyautogui.press(["tab","enter"])
        time.sleep(6) 
        Sendmessage.confirmation(name,message)

    def whatsappmessage(c):
        open_whatsapp = OpenApplications.APP_MAP["whatsapp"]() # till now only for whatsapp
        time.sleep(3)
        if "a message" in c:
            text = c.lower().split("a message",1) # example send a message to "name" "message" 
        elif "message" in c:
            text = c.lower().split("message",1)


        name_uselesstext = text[0].strip()
        name_message = text[1].strip() 

        # example send a message to "name" "message" 
        # send a message to "name" on whatsapp how are you
        # Send "name" a message how are you  1.........
        # Send "name" a message how are you on whatsapp
        # problem name can be ram, ram 123 , ram sharma , ram sharma 12c then "message"
        if "send" in name_uselesstext:
            name = name_uselesstext[5:].strip() #send name
            message = name_message                                    
            Sendmessage.find_name(name,message)

            
