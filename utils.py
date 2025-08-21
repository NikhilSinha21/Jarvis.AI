import json
import os

def get_file():
    """Load command_vocab.json and return its data"""
    file_path = "command_vocab.json"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return {}

    with open(file_path, "r") as f:
        data = json.load(f)

    return data
