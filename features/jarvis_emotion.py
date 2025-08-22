import random
import re

class JarvisEmotion:
    def add_fillers(text: str) -> str:
        fillers = ["ummm", "uhhh", "hmmm", "aaaah", "you know"]

        def insert_filler(match):
            if random.random() < 0.4:  # 40% chance
                filler = random.choice(fillers)
                # add pause after filler for realism
                return f"{match.group(0)} {filler}..."
            return match.group(0)

        # Insert fillers at commas and full stops
        text = re.sub(r'([,.])', insert_filler, text)
        return text
