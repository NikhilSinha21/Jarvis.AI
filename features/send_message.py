
# example send a message to "name" "message" 
# send a message to "name" on whatsapp how are you
# Send "name" a message how are you  1.........
# Send "name" a message how are you on whatsapp
#send rahul a message seema is here 
# send a message to rahul seema is here 
# send rahul seema is here
# seema is here message it to rahul
# rahul seema is here on whatsapp
# problem name can be ram, ram 123 , ram sharma , ram sharma 12c then "message"
# if not logged in speak please log in to send message

import pygetwindow as gw
import time 
import pyautogui
from features.jarvis_voice import JarvisVoice
from features.open_applications import OpenApplications
import keyboard
class Sendmessage:
    def open_whatsapp(): #opens whatsapp
        try:
            OpenApplications.APP_MAP["whatsapp"]()
            time.sleep(6)
            Sendmessage.screen_max()
        except Exception as e:
            print(f"can't find Whatsapp{e}")


    def screen_max(): #max the screen
        screen = gw.getWindowsWithTitle("WhatsApp")[0]
        screen.activate()
        screen.maximize()
        #Sendmessage.get_coordinates()

    def search_name(n:str) -> bool:
        if "send" in n:
            name = n[5:].strip()
            if name != "" :
                pyautogui.click(x=249, y=165)
                time.sleep(1)
                pyautogui.write(name)
                time.sleep(1)
                pyautogui.press("tab")
                pyautogui.press("enter")
                return True
            else:
                JarvisVoice.speak("Please tell me the name") 
                pyautogui.hotkey("alt","f4")

                return False   

        else :
            JarvisVoice.speak("I did not understand that")

    def confirmation(timeout = 3): # no key press send messeage else abort
        start_time = time.time()
        JarvisVoice.speak(f"Sending message in {timeout} Seconds.if you want to cancel please press any key")
        while time.time() - start_time < timeout:
            if keyboard.is_pressed():
                JarvisVoice.speak("Thanks for Confirmation")
                JarvisVoice.speak("closing Whatsapp")
                pyautogui.hotkey("alt","f4")
                return False
            time.sleep(0.1)
        # No key pressed → send message
        pyautogui.press("enter")
        JarvisVoice.speak("Message sent. Closing WhatsApp.")
        pyautogui.hotkey("alt","f4")
        return True    

    def sending_message(name,message):
        if message != "":
            pyautogui.click(x=1459, y=502)
            time.sleep(1)
            pyautogui.write(message)
            time.sleep(1)
            JarvisVoice.speak(f"Are you sure you want to send message to{name}")
            Sendmessage.confirmation(timeout = 3)
        else:
            JarvisVoice.speak("No Message")
            pyautogui.hotkey("alt","f4")
     
    def whatsappmessage(c):
        if "a message" in c.lower():
            text = c.lower().split("a message",1) # a message # the message # message
            get_name = text[0].strip()
            message = text[1].strip() if len(text)>1 else ""
           
                    
            
            Sendmessage.open_whatsapp()

            result = Sendmessage.search_name(get_name)
            if result:
                Sendmessage.sending_message(get_name, message)

