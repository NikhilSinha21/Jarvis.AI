import random
import re
from nltk.sentiment import SentimentIntensityAnalyzer

class JarvisEmotion:
    sia = SentimentIntensityAnalyzer()

    fillers = {
        "positive": ["great!", "awesome!", "haha", "that’s cool"],
        "negative": ["ohh", "I see", "hmm", "sorry about that"],
        "neutral": ["umm", "uhh", "hmm", "you know"]
    }

    @staticmethod
    def analyze(text: str) -> str:
        """Return sentiment as positive, negative, or neutral"""
        score = JarvisEmotion.sia.polarity_scores(text)
        if score['compound'] > 0.05:
            return "positive"
        elif score['compound'] < -0.05:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def add_fillers(text: str, sentiment: str = None) -> str:
        """Add random fillers based on sentiment"""
        if sentiment is None:
            sentiment = JarvisEmotion.analyze(text)
        chosen_fillers = JarvisEmotion.fillers[sentiment]

        def insert_filler(match):
            if random.random() < 0.4:  # 40% chance
                return f"{match.group(0)} {random.choice(chosen_fillers)}"
            return match.group(0)

        # Add fillers after commas & periods
        text = re.sub(r'([,.])', insert_filler, text)
        return text
