from datetime import datetime
from NewsApi import db


class NewsSentimentMetaData(db.Model):
    __tablename__ = 'sentiment_meta_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Integer)
    keywords = db.Column(db.String(255))
    sources = db.Column(db.String(255))
    total_number_of_news_articles = db.Column(db.Integer)
    positive_news_percentage = db.Column(db.Integer)
    negative_news_percentage = db.Column(db.Integer)
    neutral_news_percentage = db.Column(db.Integer)
    time_accessed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(NewsSentimentMetaData, self).__init__(**kwargs)

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {'time_accessed': self.time_accessed,
                'neutral_news_percentage': self.neutral_news_percentage,
                'negative_news_percentage': self.negative_news_percentage,
                'positive_news_percentage': self.positive_news_percentage,
                'total_number_of_news_articles': self.total_number_of_news_articles,
                'sources': self.sources,
                'keywords': self.keywords,
                'username': self.username,
                'id': self.id
                }

    @classmethod
    def filter_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def filter_by_keywords(cls, keywords):
        return cls.query.filter_by(keywords=keywords).first()

    def __repr__(self):
        return '<NewsSentimentMetaData %r>' % self.keywords


class NewsEmotionsMetaData(db.Model):
    __tablename__ = 'news_emotions_meta_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Integer)
    keywords = db.Column(db.String(255))
    sources = db.Column(db.String(255))
    total_number_of_news_articles = db.Column(db.Integer)
    happy_percentage = db.Column(db.Integer)
    angry_percentage = db.Column(db.Integer)
    sad_percentage = db.Column(db.Integer)
    surprise_percentage = db.Column(db.Integer)
    fear_percentage = db.Column(db.Integer)
    time_accessed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(NewsEmotionsMetaData, self).__init__(**kwargs)

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {'id': self.id,
                'username': self.username,
                'keywords': self.keywords,
                'sources': self.sources,
                'total_number_of_news_articles': self.total_number_of_news_articles,
                'happy_percentage': self.happy_percentage,
                'angry_percentage': self.angry_percentage,
                'sad_percentage': self.sad_percentage,
                'surprise_percentage': self.surprise_percentage,
                'fear_percentage': self.fear_percentage,
                'time_accessed': self.time_accessed
                }

    @classmethod
    def filter_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def filter_by_keywords(cls, keywords):
        return cls.query.filter_by(keywords=keywords).first()

    def __repr__(self):
        return '<NewsEmotionsMetaData %r>' % self.keywords
