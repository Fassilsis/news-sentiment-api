from NewsApi import db
from NewsApi.news.utils.data_processor import DataProcessor
from NewsApi.news.utils.sentiment_analyzer import SentimentAnalyzer
from NewsApi.news.utils.emotion_analyzer import EmotionAnalyzer
from NewsApi.models.news_models import SentimentData
from flask import jsonify, request, make_response, Blueprint
from flask_jwt_extended import jwt_required
from newsapi import NewsApiClient
from NewsApi.api_key import api_key
from sqlalchemy import exc


news = Blueprint('news', __name__)


@news.route('/news')
@news.route('/news/home')
def home():
    return 'This is a News Api'


@news.route('/news/sentiments', methods=['GET'])
@jwt_required()
def get_news_with_sentiment():
    """
    :search parameters:
        q=None, qintitle=None, sources=None,
        domains=None, exclude_domains=None,
        from_param=None, to=None,
        language=None, sort_by=None,
        page=None, page_size=None,
    :return:
        news + sentiment
    """
    search_parameters = request.get_json()
    if search_parameters is not None:
        try:
            newsapi = NewsApiClient(api_key=api_key)
            searched_news = newsapi.get_everything(**search_parameters)

            df = DataProcessor.data_processor(searched_news)
            news_sentiment_summary = SentimentAnalyzer.news_sentiment_summary(df)
            news_sentiment = SentimentAnalyzer.news_sentiment(df)

            senti_data = SentimentData(searched_news=search_parameters['q'],
                                       sentiment_classification='x',
                                       sentiment_score='news_sentiment_summary')

            db.session.add(senti_data)
            db.session.commit()

            return make_response(jsonify(status='ok', total_results=len(df),
                                         sentiment_percentage=news_sentiment_summary,
                                         detail_info=news_sentiment), 201)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        return make_response(jsonify(error_message='No input detected'), 400)


@news.route('/news/good-news', methods=['GET'])
@jwt_required()
def get_positive_news():
    """
        :search parameters:
            q=None, qintitle=None, sources=None,
            domains=None, exclude_domains=None,
            from_param=None, to=None,
            language=None, sort_by=None,
            page=None, page_size=None,
        :return:
            positive news + sentiment
        """
    search_parameters = request.get_json()
    if search_parameters is not None:
        try:
            newsapi = NewsApiClient(api_key=api_key)
            searched_news = newsapi.get_everything(**search_parameters)

            df = DataProcessor.data_processor(searched_news)
            news_sentiment = SentimentAnalyzer.positive(df)
            return make_response(jsonify(status='ok',
                                         total_results=len(news_sentiment),
                                         detail_info=news_sentiment), 201)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        return make_response(jsonify(error_message='No input detected'), 400)


@news.route('/news/emotions', methods=['GET'])
@jwt_required()
def get_emotions():
    """
        :search parameters:
            q=None, qintitle=None, sources=None,
            domains=None, exclude_domains=None,
            from_param=None, to=None,
            language=None, sort_by=None,
            page=None, page_size=None,
        :return:
            news + emotions
        """
    search_parameters = request.get_json()
    if search_parameters is not None:
        try:
            newsapi = NewsApiClient(api_key=api_key)
            searched_news = newsapi.get_everything(**search_parameters)

            df = DataProcessor.data_processor(searched_news)
            summary = EmotionAnalyzer.emotions_summary(df)
            emotions = EmotionAnalyzer.news_emotions(df)
            return make_response(jsonify(status='ok',
                                         total_results=len(emotions),
                                         detail_info=emotions,
                                         emotion_summary=summary), 201)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        return make_response(jsonify(error_message='No input detected'), 400)
