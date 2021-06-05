import pytest
import os
from NewsApi.app import app, db
from NewsApi import models
from NewsApi.api_key import api_key
from newsapi import NewsApiClient


@pytest.fixture
def client():
    """
    Create a temporary db with some data in it for using in the tests.
    """
    app.config["TESTING"] = True
    app.testing = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        newsapi = NewsApiClient(api_key=api_key)
        top_headlines = newsapi.get_top_headlines(sources='bbc-news')
        articles = top_headlines['articles']
        for i in range(len(articles)):
            my_articles = articles[i]
            news_headline = models.Headlines(author=my_articles['author'], content=my_articles['content'],
                                             description=my_articles['description'],
                                             publishedAt=my_articles['publishedAt'],
                                             source=my_articles['source'], title=my_articles['title'],
                                             url=my_articles['url'], urlToImage=my_articles['urlToImage'])
            db.session.add(news_headline)
        db.session.commit()

    yield client

    os.remove('test.sqlite')


def test_latest_article(client):
    response = client.get("/latest-article")
    assert response.json == {"response": "OK"}


@app.route('/not-found')
def testing():
    raise MissingUserError()

ext = JSONExceptionHandler(app)
ext.register(code_or_exception=MissingUserError)

with app.app_context():
    with app.test_client() as c:
        rv = c.get('/not-found')

assert rv.status_code == 404
assert rv.headers['content-type'] == 'application/json'
assert json.loads(rv.data)['message'] == 'No such user exists.'