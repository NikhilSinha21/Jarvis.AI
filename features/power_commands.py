import subprocess
import time
import keyboard
from features.jarvis_voice import JarvisVoice
class Power:

    @staticmethod
    def confirm_with_delay(action_text, delay=3):
        """Shows countdown and cancels if ANY recognized key is pressed."""
        JarvisVoice.speak(f"{action_text} in {delay} seconds. Press any key to cancel.")
        
        # Minimal safe key list (works across most layouts)
        all_keys = [
            "esc","enter","space",
            "ctrl","shift","alt",
            "tab","caps lock","backspace",
            "up","down","left","right",
            "delete",
            "f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12",
            "0","1","2","3","4","5","6","7","8","9",
            "a","b","c","d","e","f","g","h","i","j","k","l","m",
            "n","o","p","q","r","s","t","u","v","w","x","y","z"
        ]

        start_time = time.time()
        while time.time() - start_time < delay:
            for key in all_keys:
                try:
                    if keyboard.is_pressed(key):
                        JarvisVoice.speak(f"{action_text} cancelled.")
                        return False
                except:
                    pass  # ignore unrecognized keys
            time.sleep(0.05)

        return True

    
    @staticmethod
    def shutdown():
         if Power.confirm_with_delay("shutdown",delay=3):    
            subprocess.run(["shutdown", "/s", "/t", "0"])

    @staticmethod
    def restart():
        if Power.confirm_with_delay("restart",delay=3):
            subprocess.run(["shutdown", "/r", "/t", "0"])

    @staticmethod
    def signout():
        if Power.confirm_with_delay("signout",delay=3):
            subprocess.run(["shutdown", "/l"])

    @staticmethod
    def lock():
        import ctypes
        if Power.confirm_with_delay("lock",delay=3):
            ctypes.windll.user32.LockWorkStation()
        

    @staticmethod
    def sleep():
        if Power.confirm_with_delay("sleep",delay=3):
             try:
                import ctypes
                ctypes.windll.powrprof.SetSuspendState(False, True, False)
             except Exception:
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "Sleep"])
    


    def power_command(c): 
        if c.lower().startswith("system"):
            command = c[7:].strip()
            
            if "shutdown" in command.lower() or "power off" in command.lower():
                Power.shutdown()

            elif "restart" in command.lower() or "reboot" in command.lower():
                Power.restart()

            elif "sign out" in command.lower() or "log off" in command.lower() or "log out" in command.lower():
                Power.signout()

            elif "lock" in command.lower() or "lock screen" in command.lower() or "lock the screen" in command.lower():
                Power.lock()

            elif "sleep" in command.lower():
                Power.sleep()
        else: 
              JarvisVoice.speak("command not clear")      

