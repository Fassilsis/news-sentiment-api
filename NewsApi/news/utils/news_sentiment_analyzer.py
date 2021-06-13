"""
    This file contains sentiment analysis models
"""
import json
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    @staticmethod
    def classifier(df):
        nltk.download('vader_lexicon')
        sia = SentimentIntensityAnalyzer()
        df['Sentiments'] = df['description'].apply(lambda i: sia.polarity_scores(i))
        df = pd.concat([df.drop(['Sentiments'], axis=1), df['Sentiments'].apply(pd.Series)], axis=1)
        df['sentiment_score'] = df['compound']
        df['sentiment_classification'] = df['sentiment_score'].apply(lambda x: 'positive' if x > 0 else 'neutral' if x == 0 else 'negative')
        df = df.drop(['compound', 'pos', 'neu', 'neg', 'description'], axis=1)
        return df

    @staticmethod
    def news_sentiment(df):
        df = SentimentAnalyzer.classifier(df)
        result = df.to_json(orient='records')
        parsed = json.loads(result)
        return parsed

    @staticmethod
    def positive(df):
        df = SentimentAnalyzer.classifier(df)
        positive = df[(df.sentiment_classification == 'positive')]
        result = positive.to_json(orient='records')
        parsed = json.loads(result)
        return parsed

    @staticmethod
    def news_sentiment_summary(df):
        df = SentimentAnalyzer.classifier(df)
        sentiment_count = pd.DataFrame(df.sentiment_classification.value_counts())
        sentiment_percentage = 100 * sentiment_count.sentiment_classification / sentiment_count.sentiment_classification.sum()
        result = sentiment_percentage.to_json(orient='index')
        parsed = json.loads(result)
        return parsed
