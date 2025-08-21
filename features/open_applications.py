
import subprocess
import utils

class OpenApplications:
    data = utils.get_file()
            # Map of safe apps with exact execution method
    APP_MAP = {
        "camera": lambda: subprocess.Popen(["start", "microsoft.windows.camera:"], shell=True),
        "vscode": lambda: subprocess.Popen(["code"]),
        "visual studio code": lambda: subprocess.Popen(["code"]),
        "file explorer": lambda: subprocess.Popen(["explorer"]),
        "my files": lambda: subprocess.Popen(["explorer"]),
        "notepad": lambda: subprocess.Popen(["notepad"]),
        "paint": lambda: subprocess.Popen(["mspaint"]),
        "calculator": lambda: subprocess.Popen(["calc"]),
        "cmd": lambda: subprocess.Popen(["cmd"]),
        "terminal": lambda: subprocess.Popen(["wt"]),
        "control panel": lambda: subprocess.Popen(["control"]),
        "task manager": lambda: subprocess.Popen(["taskmgr"]),
        "word": lambda: subprocess.Popen([r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"]),
        "excel": lambda: subprocess.Popen([r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"]),
        "powerpoint": lambda: subprocess.Popen([r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"]),
        "spotify": lambda: subprocess.Popen(["spotify"]),
        "whatsapp": lambda: subprocess.Popen(["explorer.exe", "shell:appsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"])
    }

    @staticmethod
    def is_known_app(name: str) -> bool:
        return name.lower() in OpenApplications.APP_MAP

    @staticmethod
    def open_app(c: str):
        open_keywords = OpenApplications.data["open"]["app"] 
        
    # Normalize command
        cmd_lower = c.lower()

        # Look for app names inside APP_MAP
        for app_name in OpenApplications.APP_MAP.keys():
            if app_name in cmd_lower:   # <-- check if user said the app name
                try:
                    OpenApplications.APP_MAP[app_name]()
                    print(f"Opening {app_name}")
                    return True
                except Exception as e:
                    print(f"Failed to open '{app_name}': {e}")
                    return False

        print("No known app found in command.")
        return False