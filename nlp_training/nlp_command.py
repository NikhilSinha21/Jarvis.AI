import spacy
from features.power_commands import Power
from features.open_website import OpenWebsite
from features.send_message import Sendmessage
from features.open_applications import OpenApplications
from features.search_things_ddg import SearchThingsDDG
from features.jarvis_llm import Jarvis_LLM
import utils

class NlpTrain:
    nlp = spacy.load("en_core_web_md")
    data = utils.get_file()
    jarvis_llm = Jarvis_LLM(data)

    @staticmethod
    def nlp_for_power_command(command_text):
        doc = NlpTrain.nlp(command_text)
        print("Command:", doc.text)

        negative = any(token.dep_ == "neg" for token in doc)
        tokens = [token.lemma_.lower() for token in doc if not token.is_punct]
        print("Lemmas detected:", tokens)

        # Build single + two-word phrases
        phrases = set(tokens)
        for i in range(len(tokens)-1):
            phrases.add(f"{tokens[i]} {tokens[i+1]}")
        print("Phrases detected:", phrases)

        # Iterate over categories and intents
        for category, intents_dict in NlpTrain.data.items():
            print("Category:", category)
            for intent, keywords in intents_dict.items():
                print("Run intent:", intent)
                
                # Power commands
                if any(keyword.lower() in phrases for keyword in keywords):
                    print(f"Matched intent: {intent} in category: {category}")
                    if negative:
                        print(f"No command executed for {intent}")
                        return True
                    if hasattr(Power, intent):
                        getattr(Power, intent)()
                        return True

                # Open website/app
                if category == "open" and intent in ["website", "app"]:
                    if any(keyword.lower() in command_text.lower() for keyword in keywords):
                        if intent == "website":
                            website = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "PRODUCT")]
                            if website:
                                print(f"Opening {website[0]}")
                                OpenWebsite.process_command(website[0])
                                return True
                        elif intent == "app":
                            print(f"Opening {command_text}")
                            OpenApplications.open_app(command_text)

                # Web search using LLM
                if category == "search" and intent == "web":
                    print("Triggering web search via LLM...")
                    NlpTrain.jarvis_llm.data_clean(command_text)

        print("Sorry, I could not handle that command.")
        return False
