'''
import spacy
from features.power_commands import Power 
from features.jarvis_voice import JarvisVoice
from utils import load_json
class NlpTrain:
    nlp = spacy.load("en_core_web_sm")
    Command_Vocab_File = "command_vocab.json"
    CommandVocab = load_json(Command_Vocab_File)
    
    learner = WordLearner(Command_Vocab_File,CommandVocab)
    
    @staticmethod
    def nlp_for_power_command(c):
        doc = NlpTrain.nlp(c.lower())

        # Detect negation
        negated = any(token.dep_ == "neg" for token in doc)

        # Collect lemmas
        lemmas = {
            token.lemma_ for token in doc
            if token.pos_ in {"VERB","NOUN"} and not token.is_stop and not token.is_punct
        }

        for category, keywords in NlpTrain.CommandVocab.items():
            if set(keywords) & lemmas:
                if negated:
                    JarvisVoice.speak(f"Okay, I won’t {category} your PC.")
                    return True   # success (even if negated)

                # Execute matched action
                if hasattr(Power, category):
                    getattr(Power, category)()
                    return True   # success

        return False 

 '''
import spacy
from features.jarvis_voice import JarvisVoice
import json
from features.power_commands import Power
# can you please turn off my pc?
# dep_ sees for negative words

class NlpTrain:
    nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def nlp_for_power_command(c):
        doc = NlpTrain.nlp(c.lower())
 
        negative = any(token.dep_ == "neg" for token in doc)
        
        
        

        # Get tokens (lemmas)
        tokens = [token.lemma_ for token in doc if not token.is_punct]
        
        # Build single + two-word phrases
        phrases = set(tokens)
        for i in range(len(tokens)-1):
            phrases.add(f"{tokens[i]} {tokens[i+1]}")

        print("Lemmas detected:", tokens)
        print("Phrases detected:", phrases)
    
        with open("command_vocab.json") as f: 
            data = json.load(f)
            print("file read")
        for category, intents_dict in data.items():
            for intent, keywords in intents_dict.items():
               # for keyword in keywords:
               #     if keyword in phrases:
                if any(keyword in phrases for keyword in keywords):
                    print(f"Matched intent: {intent} in category: {category}")
                    if negative:
                        JarvisVoice.speak(f"No command executed for {intent}")
                        return True
                    if hasattr(Power, intent):
                        getattr(Power, intent)()
                        return True
        print("sorry")        
        return False    
           


