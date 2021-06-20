from NewsApi.news.utils.news_data_processor import NewsDataProcessor
from NewsApi.news.utils.news_sentiment_analyzer import SentimentAnalyzer
from NewsApi.news.utils.news_emotion_analyzer import EmotionAnalyzer
from NewsApi.models.news_models import NewsSentimentMetaData, NewsEmotionsMetaData
from NewsApi.models.user_models import User
from flask import jsonify, request, make_response, Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from newsapi import NewsApiClient
from NewsApi.api_key import api_key
from sqlalchemy import exc


news = Blueprint('news', __name__)
news_api = NewsApiClient(api_key=api_key)


@news.route('/')
@news.route('/home')
def home():
    return render_template('index.html')


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
            searched_news = news_api.get_everything(**search_parameters)

            df = NewsDataProcessor.get_news_data(searched_news)
            news_sentiment_summary = SentimentAnalyzer.news_sentiment_summary(df)
            news_sentiment = SentimentAnalyzer.news_sentiment(df)

            data = NewsSentimentMetaData(username=get_jwt_identity(),
                                         keywords=search_parameters["q"],
                                         sources=search_parameters["sources"],
                                         total_number_of_news_articles=len(df),
                                         positive_news_percentage=news_sentiment_summary["positive"],
                                         negative_news_percentage=news_sentiment_summary["negative"],
                                         neutral_news_percentage=news_sentiment_summary["neutral"])

            data.add_to_db()

            return make_response(jsonify(status='ok', total_results=len(df),
                                         sentiment_percentage=news_sentiment_summary,
                                         detail_info=news_sentiment), 201)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        return make_response(jsonify(message='No input detected'), 400)


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
            searched_news = news_api.get_everything(**search_parameters)

            df = NewsDataProcessor.get_news_data(searched_news)
            news_sentiment = SentimentAnalyzer.positive(df)
            return make_response(jsonify(status='ok',
                                         total_results=len(news_sentiment),
                                         detail_info=news_sentiment), 201)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        return make_response(jsonify(message='No input detected'), 400)


@news.route('/news/emotions', methods=['GET'])
@jwt_required()
def get_news_emotions():
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
            searched_news = news_api.get_everything(**search_parameters)

            df = NewsDataProcessor.get_news_data(searched_news)
            summary = EmotionAnalyzer.emotions_summary(df)
            emotions = EmotionAnalyzer.news_emotions(df)

            data = NewsEmotionsMetaData(username=get_jwt_identity(),
                                        keywords=search_parameters["q"],
                                        sources=search_parameters["sources"],
                                        total_number_of_news_articles=len(df),
                                        happy_percentage=summary["Happy"],
                                        angry_percentage=summary["Angry"],
                                        sad_percentage=summary["Sad"],
                                        surprise_percentage=summary["Surprise"],
                                        fear_percentage=summary["Fear"])
            data.add_to_db()

            return make_response(jsonify(status='ok',
                                         total_results=len(df),
                                         detail_info=emotions,
                                         emotion_summary=summary), 201)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        return make_response(jsonify(error_message='No input detected'), 400)


@news.route('/news/happy-news', methods=['GET'])
@jwt_required()
def get_happy_news():
    """
        :search parameters:
            q=None, qintitle=None, sources=None,
            domains=None, exclude_domains=None,
            from_param=None, to=None,
            language=None, sort_by=None,
            page=None, page_size=None,
        :return:
            happy news + emotions
        """
    search_parameters = request.get_json()
    if search_parameters is not None:
        try:
            searched_news = news_api.get_everything(**search_parameters)

            df = NewsDataProcessor.get_news_data(searched_news)
            happy_news = EmotionAnalyzer.happy(df)
            return make_response(jsonify(status='ok',
                                         total_results=len(happy_news),
                                         detail_info=happy_news), 201)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        return make_response(jsonify(message='No input detected'), 400)


@news.route('/news/emotions-metadata', methods=['GET'])
@jwt_required()
def get_all_news_emotions_metadata():

    if User.query.filter_by(role_name='admin').first():
        try:
            metadata = list(map(lambda x: x.serialize(), NewsEmotionsMetaData.query.all()))
            total = NewsEmotionsMetaData.query.count()
            return make_response(jsonify(metadata=metadata, total=total), 200)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        try:
            metadata = list(map(lambda x: x.serialize(), NewsEmotionsMetaData.query.filter_by(username=get_jwt_identity()).all()))
            total = NewsEmotionsMetaData.query.filter_by(username=get_jwt_identity()).count()
            return make_response(jsonify(metadata=metadata, total=total), 200)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)


@news.route('/news/sentiments-metadata', methods=['GET'])
@jwt_required()
def get_all_news_sentiments_metadata():

    if User.query.filter_by(role_name='admin').first():
        try:
            metadata = list(map(lambda x: x.serialize(), NewsSentimentMetaData.query.all()))
            total = NewsSentimentMetaData.query.count()
            return make_response(jsonify(metadata=metadata, total=total), 200)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
    else:
        try:
            metadata = list(map(lambda x: x.serialize(), NewsSentimentMetaData.query.filter_by(username=get_jwt_identity()).all()))
            total = NewsSentimentMetaData.query.filter_by(username=get_jwt_identity()).count()
            return make_response(jsonify(metadata=metadata, total=total), 200)
        except exc.SQLAlchemyError as e:
            return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
        except Exception as e:
            return make_response(jsonify(error_message=str(e)), 400)
