'''
import spacy
from spacy.training.example import Example
import json
from sklearn.model_selection import train_test_split
import shutil
import os

# -----------------------------
# Delete previous model
# -----------------------------
shutil.rmtree("./custom_nlp_model", ignore_errors=True)
print("Old model deleted.")

# -----------------------------
# Load training data from JSON
# -----------------------------
class get_data:
    @staticmethod
    def get_data_from_json_file():
        with open("Training_data.json", "r", encoding="utf-8") as f:
            TrainingData = json.load(f)
        # Convert JSON to format [(text, {"entities": [...]})]
        TrainingData = [(item["text"], {"entities": item["entities"]}) for item in TrainingData]
        return TrainingData     

# -----------------------------
# Helper function to align entities
# -----------------------------
def get_aligned_entities(doc, entities):
    aligned_entities = []
    for start, end, label in entities:
        span = doc.char_span(start, end, label=label)
        if span is not None:
            aligned_entities.append((span.start_char, span.end_char, label))
        else:
            print(f"Skipping misaligned entity: {doc.text[start:end]}")
    return aligned_entities

# -----------------------------
# Model Training
# -----------------------------
class ModelTraining:
    def __init__(self, model_name=None, epochs=35):
        # Use multilingual model if model_name is None
        if model_name and os.path.exists(model_name):
            self.nlp = spacy.load(model_name)
        else:
            print("Using blank multilingual model...")
            self.nlp = spacy.blank("xx")  # multilingual model

        # Check if NER exists, otherwise add
        if "ner" not in self.nlp.pipe_names:
            self.ner = self.nlp.add_pipe("ner", last=True)
        else:
            self.ner = self.nlp.get_pipe("ner")

        # Load and split data
        self.TRAIN_DATA = get_data.get_data_from_json_file()
        self.train_data, self.valid_data = train_test_split(
            self.TRAIN_DATA, test_size=0.2, random_state=42
        )

        # Add labels dynamically from training data
        for _, annotations in self.TRAIN_DATA:
            for ent in annotations["entities"]:
                self.ner.add_label(ent[2])

        # Initialize optimizer
        self.optimizer = self.nlp.begin_training()
        self.epochs = epochs

    def train(self):
        for epoch in range(self.epochs):
            losses = {}
            skipped = 0
            # Training
            for text, annotations in self.train_data:
                doc = self.nlp.make_doc(text)
                aligned_entities = get_aligned_entities(doc, annotations["entities"])
                if not aligned_entities:
                    skipped += 1
                    continue

                example = Example.from_dict(doc, {"entities": aligned_entities})
                self.nlp.update([example], sgd=self.optimizer, losses=losses, drop=0.3)

            print(f"Epoch {epoch+1} Training Losses: {losses}")
            print(f"Skipped {skipped} misaligned examples this epoch.")

            # Validation
            correct = 0
            total = 0
            for text, annotations in self.valid_data:
                doc = self.nlp(text)
                pred_ents = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
                true_entities = get_aligned_entities(doc, annotations["entities"])
                total += len(true_entities)
                for ent in pred_ents:
                    if ent in true_entities:
                        correct += 1

            accuracy = correct / total if total > 0 else 0
            print(f"Validation Accuracy: {accuracy:.2f}")

        # Save the trained model
        self.nlp.to_disk("./custom_nlp_model")
        print("Model saved to ./custom_nlp_model")

# -----------------------------
# Run training
# -----------------------------
if __name__ == "__main__":
    #trainer = ModelTraining()
    #trainer.train()

    #import shutil

    #Delete the previous trained model folder
    shutil.rmtree("./custom_nlp_model")
    print("Previous model deleted successfully.")
'''