from ddgs import DDGS
from features.jarvis_voice import JarvisVoice
import utils
import regex as re 
import wikipedia
import webbrowser
from features.jarvis_emotion import JarvisEmotion

class SearchThingsDDG:
    data = utils.get_file()
    @staticmethod
    def clean_query(command: str):
        command = command.lower().strip()

        # go through all "search" keywords
        for keyword in SearchThingsDDG.data["search"]["web"] + SearchThingsDDG.data["search"]["image"]:
            if keyword in command:
                # split on the keyword and take everything after it
                parts = command.split(keyword, 1)
                if len(parts) > 1:
                    cleaned = parts[1].strip()
                    # ✅ directly call internet_qa_with_image here
                    return SearchThingsDDG.internet_qa_with_image(cleaned)

        # if no keyword found → still call search with original command
        return SearchThingsDDG.internet_qa_with_image(command)
    
    @staticmethod
    def internet_qa_with_image(query):
        clean_query = query.strip()
        print(query)
        print("internet_qa_with_image")
        image = ""
        about = ""

        try:
            about = wikipedia.summary(clean_query, sentences=2)
        except:

        # text search
            with DDGS() as ddgs:
                result = list(ddgs.text(query, max_results=3))  # wrap in list
                result = list(ddgs.text(clean_query, max_results=3))
                if result:
                    about = result[0].get("body") or result[0].get("title") or ""
                    # Remove timestamps like "5 hours ago"
                    about = re.sub(r'\d+\s+(hour|hours|minute|minutes|day|days)\s+ago', '', about, flags=re.IGNORECASE)
                    about = about.strip()


        # image search
        with DDGS() as ddgs:
            ifimage = list(ddgs.images(query, max_results=3))  # wrap in list
            if ifimage:
                image = ifimage[0]["image"]

        lines = about.split('. ')  # split by sentences
        speak_text = '. '.join(lines[:2])  # first 2 sentences
        if speak_text:
            print(speak_text)
            emotional_text = JarvisEmotion.add_fillers(speak_text)
            JarvisVoice.speak(emotional_text + ". Here’s more information about it and image as well")
        

        # combine results
        if about and image:
            msg = f"{about} \n Image url {image}"
            webbrowser.open(image)
            print(msg)
            return msg

        elif about:
            print(about)
            return about

        elif image:
            msg = f"{image} — sorry, I cannot find anything about it"
            print(msg)
            JarvisVoice.speak("Sorry, I cannot find anything about it, but here is an image.")
            webbrowser.open(image)
            return msg

        else:
            msg = "Sorry, no data found on internet."
            print(msg)
            JarvisVoice.speak(msg)
            return msg
