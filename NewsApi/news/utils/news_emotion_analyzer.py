import json
import pandas as pd
import text2emotion


class EmotionAnalyzer:
    @staticmethod
    def emotions(df):
        df['emotions'] = df['description'].apply(lambda i: text2emotion.get_emotion(i))
        df = pd.concat([df.drop(['emotions'], axis=1), df['emotions'].apply(pd.Series)], axis=1)
        df = df.drop(['description'], axis=1)
        return df

    @staticmethod
    def news_emotions(df):
        df = EmotionAnalyzer.emotions(df)
        result = df.to_json(orient='records')
        parsed = json.loads(result)
        return parsed

    @staticmethod
    def happy(df):
        df = EmotionAnalyzer.emotions(df)
        happy_news = df.loc[(df.Happy >= 0.4)]
        result = happy_news.to_json(orient='records')
        parsed = json.loads(result)
        return parsed

    @staticmethod
    def emotions_summary(df):
        df = EmotionAnalyzer.emotions(df)
        emotion_percentage = 100*(df.mean(axis=0, numeric_only=True))
        result = emotion_percentage.to_json(orient='index')
        parsed = json.loads(result)
        return parsed