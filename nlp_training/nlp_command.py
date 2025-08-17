import spacy
from features.jarvis_voice import JarvisVoice
import json
from features.power_commands import Power
from features.open_website import OpenWebsite
# can you please turn off my pc?
# dep_ sees for negative words

class NlpTrain:
    nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def nlp_for_power_command(c): # can you please open youtube
        doc = NlpTrain.nlp(c) # Can You Please Open Youtube
        print(doc)
                      

        negative = any(token.dep_ == "neg" for token in doc)
        # Get tokens (lemmas)
        tokens = [token.lemma_.lower() for token in doc if not token.is_punct] # can you please open youtube
        print("Lemmas detected:", tokens)
        # Build single + two-word phrases
        phrases = set(tokens) #'can you', 'open', 'you', 'open youtube', 'please open', 'youtube', 'please', 'can', 'you please'
        for i in range(len(tokens)-1):
            phrases.add(f"{tokens[i]} {tokens[i+1]}")

        print("Phrases detected:", phrases)#'can you', 'open', 'you', 'open youtube', 'please open', 'youtube', 'please', 'can', 'you ple ase'
    
        with open("command_vocab.json") as f: 
            data = json.load(f)
            print("file read")

        for category, intents_dict in data.items():
            #to run power related commands
            print("category")
            for intent, keywords in intents_dict.items():
               # for keyword in keywords:
               #     if keyword in phrases:
                # match power commands
                print("run")
                if any(keyword.lower() in phrases for keyword in keywords):   # please open   open youtube
                    print(f"Matched intent: {intent} in category: {category}")
                    if negative:
                        JarvisVoice.speak(f"No command executed for {intent}")
                        return True
                    if hasattr(Power, intent):
                        getattr(Power, intent)()
                        return True

                if category == "open" and intent == "website" :  
                    print("open run")
                    # match power commands
                    if any(keyword.lower() in c.lower() for keyword in keywords): #can you   you please   please open   open youtube   can  you  please  open   youtube 
                        print("hi ha ha ha")
                        proper_nouns = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

                        if not proper_nouns:
                            proper_nouns = [doc[-1].text]

                        if proper_nouns:
                            print("gi ha ha ah")
                            
                            JarvisVoice.speak(f"Opening {proper_nouns[0]}")
                            OpenWebsite.process_command(proper_nouns[0])
                            return True
                else:
                    print("cry")            
                        
        print("sorry")        
        return False    

