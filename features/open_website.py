
import webbrowser
import requests

class OpenWebsite:
    @staticmethod
    def opens_url(site_name: str):
        url = f"https://{site_name}.com"
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                webbrowser.open(url)
            else:
                webbrowser.open(f"https://{site_name}.in")
        except Exception:
            webbrowser.open(f"https://{site_name}.in")

    @staticmethod
    def process_command(c: str):
        command = c[5:].strip().replace(" ", "")
        if "." not in command:
            OpenWebsite.opens_url(command)
        else:
            try:
                webbrowser.open(f"https://{command}")
            except Exception as e:
                print(f"Error opening direct URL: {e}")


