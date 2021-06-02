from NewsApi.app import app, db
from NewsApi.sentiment_analyzer import SentimentAnalyzer
from NewsApi import models
from flask import jsonify, request, make_response, render_template
from newsapi import NewsApiClient
from NewsApi.api_key import api_key
from sqlalchemy.orm import load_only


@app.route('/')
def home():
    return 'This is a News Api'


@app.route('/register', methods=['POST'])
def register():
    new_user = models.User(username=request.json['username'],
                           email=request.json['email'])
    if not new_user:
        make_response(jsonify(error='Username and email required.'), 201)

    else:
        db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(response='OK'), 201)


@app.route('/query/<q>')
def headlines(q):
    newsapi = NewsApiClient(api_key=api_key)
    top_headlines = newsapi.get_everything(q=q)
    top_headlines = top_headlines['articles']
    return jsonify(top_headlines= top_headlines)

@app.route('/news')
def titles():
    newsapi = NewsApiClient(api_key=api_key)
    top_headlines = newsapi.get_top_headlines(sources='bbc-news')
    articles = top_headlines['articles']
    news = []

    for i in range(len(articles)):
        my_articles = articles[i]
        news.append({'title': my_articles['title'], 'description': my_articles['description']})

    return jsonify({'news': news})


@app.route('/latest-article')
def latest_article():
    newsapi = NewsApiClient(api_key=api_key)
    top_headlines = newsapi.get_top_headlines(sources='bbc-news')
    articles = top_headlines['articles']
    for i in range(len(articles)):
        my_articles = articles[i]
        news_headline = models.Headlines(author=my_articles['author'], content=my_articles['content'],
                                         description=my_articles['description'], publishedAt=my_articles['publishedAt'],
                                         source=my_articles['source'], title=my_articles['title'],
                                         url=my_articles['url'], urlToImage=my_articles['urlToImage'])
        db.session.add(news_headline)
    db.session.commit()
    return make_response(jsonify(response='OK'), 201)

@app.route('/get-news-headlines', methods=['GET'])
def get_news_headlines():

    """
    This function creates the list of news headlines from our data
    """
    news_headlines = models.Headlines.query.order_by(models.Headlines.id).all()

    # Serialize the data for the response
    news_schema = models.HeadlinesSchema(many=True)
    return jsonify(news_schema.dump(news_headlines))

@app.route('/get-one-news-headline/<id>', methods=['GET'])
def get_one_headline(id):
    """
    This function responds to a request for /get-one-news-headline/{news_headline_id}
    with one matching news headline from the headlines.
    :param id:   ID of news headline to find
    :return:news headline matching ID
    """
    # Get the news_headline requested
    news_headline = models.Headlines.query.filter(models.Headlines.id==id).one_or_none()

    # Check if the requested id exists
    if news_headline is not None:
        # Serialize the data for the response
        news_schema = models.HeadlinesSchema()
        return make_response(jsonify(news_schema.dump(news_headline)), 201)
    else:
        return make_response(f'News Headline not found for the given Id: {id}', 404)



@app.route('/get-everything/<query>')
def get_everything(query):
    """
        This function takes data from newsapi and stores it in a database
        """
    newsapi = NewsApiClient(api_key=api_key)
    everything = newsapi.get_everything(qintitle=query)
    articles = everything['articles']
    for i in range(len(articles)):
        my_articles = articles[i]
        found_articles = models.SearchedNews(author=my_articles['author'], content=my_articles['content'],
                                         description=my_articles['description'], publishedAt=my_articles['publishedAt'],
                                         source=my_articles['source'], title=my_articles['title'],
                                         url=my_articles['url'], urlToImage=my_articles['urlToImage'])
        db.session.add(found_articles)
    db.session.commit()
    return make_response(jsonify(response='OK'), 201)


@app.route('/news-sentiment', methods=['GET'])
def news_sentiment():
    news = db.session.query(models.SearchedNews).all()
    contents = [item.content for item in news]
    text = ' '.join(contents)
    senti = SentimentAnalyzer.sentiment(text)
    score = SentimentAnalyzer.score(text)
    #return make_response(jsonify(text=text), 201)
    return make_response(jsonify(sentiment=senti, score=score), 201)





# @app.route('/news-sentiment', methods=['GET'])
# def news_sentiment():
#     description = models.SearchedNews.query.options(load_only('description')).all()
#     sentiment_schema = models.SentimentSchema()
#     return make_response(jsonify(sentiment_schema.dump(description)), 201)