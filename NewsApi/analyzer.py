"""
    This contains sentiment analysis models
"""
import json
import pandas as pd
import nltk
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import request
from newsapi import NewsApiClient
from NewsApi.api_key import api_key
from sqlalchemy import null, exc


class DataProcessor:
    @staticmethod
    def data_processing():
        keyword = request.json['keyword']
        if keyword != null and len(keyword) > 0:
            keyword = request.json['keyword']
            newsapi = NewsApiClient(api_key=api_key)
            searched_news = newsapi.get_everything(qintitle=keyword, language='en')
            articles = searched_news['articles']
            total_results = len(articles)
            title = []
            content = []
            source = []
            url = []

            for i in range(total_results):
                my_articles = articles[i]
                title.append(my_articles['title'])
                source.append(my_articles['source']['name'])
                content.append(my_articles['description'])
                url.append(my_articles['url'])

            df = pd.DataFrame(list(zip(title, source, content, url)),
                              columns=['title', 'source', 'content', 'url'])

        return df



class SentimentAnalyzer:
    @staticmethod
    def sentiment_score(text):
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(text)['compound']
        return score

    @staticmethod
    def sentiment(text):
        score = SentimentAnalyzer.sentiment_score(text)
        if score > 0:
            return 'positive'
        elif score < 0:
            return 'negative'
        else:
            return 'neutral'

    @staticmethod
    def processer(df):
        sia = SentimentIntensityAnalyzer()
        df['Sentiments'] = df['content'].apply(lambda i: sia.polarity_scores(i))
        df = pd.concat([df.drop(['Sentiments'], axis=1), df['Sentiments'].apply(pd.Series)], axis=1)
        df['sentiment_score'] = df['compound']
        df = df.drop(['compound', 'pos', 'neu', 'neg', 'content'], axis=1)
        for i in range(0, len(df)):
            if (df.loc[i, 'sentiment_score'] > 0):
                df.loc[i, 'sentiment_classification'] = 'Positive'
            elif (df.loc[i, 'sentiment_score'] < 0):
                df.loc[i, 'sentiment_classification'] = 'Negative'
            else:
                df.loc[i, 'sentiment_classification'] = 'Neutral'

        return df



    @staticmethod
    def news_sentiment(df):
        df = SentimentAnalyzer.processer(df)
        result = df.to_json(orient='records')
        parsed = json.loads(result)
        return parsed

    @staticmethod
    def positive(df):
        df = SentimentAnalyzer.processer(df)
        positive = df[(df.sentiment_classification == 'Positive')]
        result = positive.to_json(orient='records')
        parsed = json.loads(result)
        return parsed

    @staticmethod
    def news_sentiment_summary(df):
        df = SentimentAnalyzer.processer(df)
        sentiment_count = pd.DataFrame(df.sentiment_classification.value_counts())
        sentiment_percentage = 100 * sentiment_count.sentiment_classification / sentiment_count.sentiment_classification.sum()
        #sentiment_percentage['Percentage'] = sentiment_percentage.index
        result = sentiment_percentage.to_json(orient='index')
        parsed = json.loads(result)
        return parsed

# # polarity and subjectivity
# df['news_headline'] = df['news_headline'].astype(str)
# pol = lambda x: TextBlob(x).sentiment.polarity
# sub = lambda x: TextBlob(x).sentiment.subjectivity
# df['Polarity'] = df['news_headline'].apply(pol)
# df['Subjectivity'] = df['news_headline'].apply(sub)
