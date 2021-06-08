from NewsApi import db


class SentimentData(db.Model):
    __tablename__ = 'sentiment_data'
    id = db.Column(db.Integer, primary_key=True)
    searched_news = db.Column(db.String(100), nullable=False)
    sentiment_classification = db.Column(db.String(100), nullable=False)
    sentiment_score = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<SentimentData %r>' % self.searched_news