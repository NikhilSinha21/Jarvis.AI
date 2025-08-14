'''
import webbrowser
import requests

class open_website:
    @staticmethod
    def opens_url(com_in):  
        url = f"https://{com_in}.com"  # store the actual string
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                webbrowser.open(url)
            else:
                webbrowser.open(f"https://{com_in}.in")  # fallback to .in
        except Exception as e:
            print(f"Error opening URL: {e}")
            
    def process_command(c): 
        # open websites 
        if c.startswith("open"): # for the command which is given by the user contain "open" like open google 
            command =c[5:].strip() 
            command = command.replace(" ", "") #remove space from the text
            if "." not in command:
                #use in or com send message if i get 200 web is working
                open_website.opens_url(command)
                

            else: #if command is direct and clear
                try:
                    webbrowser.open(f"https://{command}")
                except Exception as e:
                    print(e)
                
        else :
            command = c.replace(" ", "")
            if "." not in command:
                #use in or com send message if i get 200 web is working
                open_website.opens_url(command)
                
            else: #if command is direct and clear
                try:
                    webbrowser.open(f"https://{command}")
                except Exception as e:
                    print(e)

'''
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


