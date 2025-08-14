import screen_brightness_control as sbc
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import platform
import re

from features.jarvis_voice import JarvisVoice

class SystemControls:
    """A class to control system features like brightness, volume"""

    @staticmethod
    def handle_system_command(command: str, controls: 'SystemControls'):
        cmd = command.lower()

        # --- Brightness ---
        if "increase brightness" in cmd:
            controls.increase_brightness()
        elif "decrease brightness" in cmd:
            controls.decrease_brightness()
        elif "set brightness" in cmd:
            match = re.search(r"\b(\d{1,3})\b", cmd)
            if match:
                value = int(match.group(1))
                controls.set_brightness(value)
            else:
                JarvisVoice.speak("Please specify a brightness value.")

        # --- Volume ---
        elif "increase volume" in cmd:
            controls.increase_volume()
        elif "decrease volume" in cmd:
            controls.decrease_volume()
        elif "set volume" in cmd:
            match = re.search(r"\b(\d{1,3})\b", cmd)
            if match:
                value = int(match.group(1))
                controls.set_volume(value)
            else:
                JarvisVoice.speak("Please specify a volume value.")

        # --- Mute / Unmute ---
        elif "unmute" in cmd:
            controls.toggle_mute()
        elif "mute" in cmd:
            controls.toggle_mute()

        else:
            JarvisVoice.speak("System command not recognized.")

    def __init__(self):
        """Initializes the audio endpoint volume for Windows and checks OS."""
        self.os_name = platform.system()
        self.volume = None
        if self.os_name == "Windows":
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
                self.volume = interface.QueryInterface(IAudioEndpointVolume)
            except Exception as e:
                print(f"Error initializing Windows audio controls: {e}")

    # --- Brightness Control ---
    def set_brightness(self, value: int):
        try:
            value = max(0, min(100, value))
            sbc.set_brightness(value, display=0)
            print(f"Brightness set to {value}%")
        except Exception as e:
            print(f"Error setting brightness: {e}")

    def increase_brightness(self, step: int = 10):
        try:
            current_brightness = sbc.get_brightness(display=0)[0]
            new_brightness = min(100, current_brightness + step)
            self.set_brightness(new_brightness)
            print(f"Increased brightness to {new_brightness}%")
        except Exception as e:
            print(f"Error increasing brightness: {e}")

    def decrease_brightness(self, step: int = 10):
        try:
            current_brightness = sbc.get_brightness(display=0)[0]
            new_brightness = max(0, current_brightness - step)
            self.set_brightness(new_brightness)
            print(f"Decreased brightness to {new_brightness}%")
        except Exception as e:
            print(f"Error decreasing brightness: {e}")
            
    # --- Volume Control (Windows Specific) ---
    def set_volume(self, value: int):
        if self.volume:
            try:
                normalized_value = max(0.0, min(1.0, value / 100.0))
                self.volume.SetMasterVolumeLevelScalar(normalized_value, None)
                print(f"Volume set to {value}%")
            except Exception as e:
                print(f"Error setting volume: {e}")
        else:
            print("Volume control is not available on this OS.")

    def increase_volume(self, step: int = 10):
        if self.volume:
            try:
                current_volume = self.volume.GetMasterVolumeLevelScalar()
                new_volume_norm = min(1.0, current_volume + (step / 100.0))
                self.volume.SetMasterVolumeLevelScalar(new_volume_norm, None)
                new_volume_percent = int(new_volume_norm * 100)
                print(f"Increased volume to {new_volume_percent}%")
            except Exception as e:
                print(f"Error increasing volume: {e}")
        else:
            print("Volume control is not available on this OS.")

    def decrease_volume(self, step: int = 10):
        if self.volume:
            try:
                current_volume = self.volume.GetMasterVolumeLevelScalar()
                new_volume_norm = max(0.0, current_volume - (step / 100.0))
                self.volume.SetMasterVolumeLevelScalar(new_volume_norm, None)
                new_volume_percent = int(new_volume_norm * 100)
                print(f"Decreased volume to {new_volume_percent}%")
            except Exception as e:
                print(f"Error decreasing volume: {e}")
        else:
            print("Volume control is not available on this OS.")

    def toggle_mute(self):
        if self.volume:
            try:
                is_muted = self.volume.GetMute()
                self.volume.SetMute(not is_muted, None)
                print(f"Volume mute state toggled to: {'Muted' if not is_muted else 'Unmuted'}")
            except Exception as e:
                print(f"Error toggling mute: {e}")
        else:
            print("Volume control is not available on this OS.")
