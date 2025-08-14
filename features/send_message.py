
'''
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

            
'''
# example send a message to "name" "message" 
# send a message to "name" on whatsapp how are you
# Send "name" a message how are you  1.........
# Send "name" a message how are you on whatsapp
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
        '''
        if any(word in c.lower() for word in ["yes", "please", "ok"]):
            JarvisVoice.speak("Thanks for Confirmation")
            pyautogui.press("enter")
            JarvisVoice.speak("All done... Now closing Whatsapp")
            pyautogui.hotkey("alt","f4")
        elif "no" in c.lower():
            JarvisVoice.speak("Thanks for Confirmation")
            JarvisVoice.speak("closing Whatsapp")
            pyautogui.hotkey("alt","f4")
        else:
            JarvisVoice.speak("voice is not clear")
            JarvisVoice.speak("closing Whatsapp")
            pyautogui.hotkey("alt","f4")    
        '''

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
    '''
    #used get_coordinates to find the coordinates of the search and message input area
    def get_coordinates():
        
        print("Move your mouse over the search box in 5 seconds...")

        x, y = pyautogui.position()
        print(f"Click coordinates: x={x}, y={y}")
    '''    
    def whatsappmessage(c):
        if "a message" in c.lower():
            text = c.lower().split("a message",1) # a message # the message # message
            get_name = text[0].strip()
            message = text[1].strip() if len(text)>1 else ""
           
                    
            
            Sendmessage.open_whatsapp()

            result = Sendmessage.search_name(get_name)
            if result:
                Sendmessage.sending_message(get_name, message)

