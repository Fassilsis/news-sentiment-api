"This contains sentiment analysis models"
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    @staticmethod
    def sentiment(text):
        nltk.download('vader_lexicon')
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(text)['compound']
        if score > 0:
            return 'positive'
        elif score < 0:
            return 'negative'
        else:
            return 'neutral'

    @staticmethod
    def score(text):
        nltk.download('vader_lexicon')
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(text)['compound']
        return score