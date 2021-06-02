from NewsApi.app import db, ma
from datetime import datetime
import logging as lg

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    status = db.Column(db.String(80))


class Headlines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=True)
    content = db.Column(db.String(3000), nullable=True)
    description = db.Column(db.String(3000), nullable=True)
    publishedAt = db.Column(db.String(600), nullable=True)
    title = db.Column(db.String(600), nullable=True)
    url = db.Column(db.String(1000), nullable=True)
    urlToImage = db.Column(db.String(1000), nullable=True)

    def __init__(self, author, content, description, source, publishedAt, title, url, urlToImage):
        self.author = author
        self.content = content
        self.description = description
        self.source = source
        self.publishedAt = publishedAt
        self.title = title
        self.url = url
        self.urlToImage = urlToImage


class HeadlinesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Headlines
        load_instance = True


class SearchedNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=True)
    content = db.Column(db.String(3000), nullable=True)
    description = db.Column(db.String(3000), nullable=True)
    publishedAt = db.Column(db.String(600), nullable=True)
    title = db.Column(db.String(600), nullable=True)
    url = db.Column(db.String(1000), nullable=True)
    urlToImage = db.Column(db.String(1000), nullable=True)

    def __init__(self, author, content, description, source, publishedAt, title, url, urlToImage):
        self.author = author
        self.content = content
        self.description = description
        self.source = source
        self.publishedAt = publishedAt
        self.title = title
        self.url = url
        self.urlToImage = urlToImage


class SearchedNewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SearchedNews
        load_instance = True

class SentimentSchema(ma.Schema):
    class Meta:
        model = SearchedNews
        load_instance = True

db.create_all()