
import json
import spacy
from features.jarvis_voice import JarvisVoice

class WordLearner:
    pass
    '''
    light_verbs = {"put", "make", "do", "go", "get", "have", "take", "pc"}

    def __init__(self, vocab_file, vocab_dic):
        self.vocab_file = vocab_file
        self.vocab = vocab_dic
        self.nlp = spacy.load("en_core_web_sm")

    def save(self):
        with open(self.vocab_file, "w") as f:
            json.dump(self.vocab, f, indent=4)

    def learn_new_words(self, command: str):
        """Process a command, extract unknown words, and learn them if user agrees."""

        doc = self.nlp(command.lower())
        candidates = [
            token.lemma_ for token in doc
            if token.pos_ in {"VERB", "NOUN"}
            and not token.is_stop and not token.is_punct
            and token.lemma_ not in self.light_verbs
        ]

        for word in candidates:
            # Check if word already known
            if any(
                word in intent_words
                for category in self.vocab.values()
                for intent_words in category.values()
            ):
                continue  # already known

            # Step 1: Ask user to confirm teaching
            JarvisVoice.speak(f"I don’t know the word '{word}'. Do you want to teach me?")
            response = JarvisVoice.listen(timeout=5, phrase_time_limit=5)
            print(f"User response: {response}")

            if not response:
                continue

            CONFIRM_WORDS = ["yes", "yeah", "yep", "ok", "okay", "sure", "right", "affirmative"]
            if not any(w in response.lower() for w in CONFIRM_WORDS):
                JarvisVoice.speak("Okay, I won’t save it.")
                continue

            # Step 2: Ask for category
            categories = ", ".join(self.vocab.keys())
            JarvisVoice.speak(f"Which category does it belong to? Options are: {categories}")
            category_ans = JarvisVoice.listen(timeout=5, phrase_time_limit=5)

            if not category_ans:
                JarvisVoice.speak("I didn’t hear a category. Cancelling learning.")
                return

            category = category_ans.lower().strip()
            if category not in self.vocab:
                JarvisVoice.speak("Invalid category. I won’t save the word.")
                return

            # Step 3: Ask for intent
            intents = ", ".join(self.vocab[category].keys())
            JarvisVoice.speak(f"Which intent inside {category}? For example: {intents}")
            intent_ans = JarvisVoice.listen(timeout=5, phrase_time_limit=5)

            if not intent_ans:
                JarvisVoice.speak("I didn’t hear an intent. Cancelling learning.")
                return

            intent = intent_ans.lower().strip()
            if intent not in self.vocab[category]:
                JarvisVoice.speak("Invalid intent. I won’t save the word.")
                return

            # Step 4: Save the new word
            if word not in self.vocab[category][intent]:
                self.vocab[category][intent].append(word)
                self.save()
                JarvisVoice.speak(f"Okay, I learned '{word}' as {intent} under {category}.")
            else:
                JarvisVoice.speak(f"I already know '{word}' under {intent}.")
'''
