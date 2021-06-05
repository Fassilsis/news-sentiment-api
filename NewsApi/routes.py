from datetime import timedelta
from NewsApi.app import app, db
from NewsApi.analyzer import SentimentAnalyzer, DataProcessor
from NewsApi.models import User, AccessToken
from flask import jsonify, request, make_response

from flask_login import login_required, login_user, logout_user
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from sqlalchemy import null, exc


@app.route('/')
@app.route('/home')
def home():
    return 'This is a News Api'


@app.route('/register', methods=['POST'])
def register():
    try:
        body = request.get_json()
        user = User(**body)

        if len(body.get("password")) >= 8:
            user.hash_password()
        else:
            return make_response(jsonify(message='Password should be at least 8 characters'), 400)

        db.session.add(user)
        db.session.commit()

        return make_response(jsonify(message='New user added successfully'), 201)
    except exc.SQLAlchemyError as e:
        return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
    except Exception as e:
        return make_response(jsonify(error_message=str(e)), 400)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        user = User.query.filter_by(email=request.json['email']).first()

        if user is not None:
            authorized = user.check_password(password=request.json['password'])
            if not authorized:
                return make_response(jsonify(error='Invalid Email or Password'), 401)
        else:
            return make_response(jsonify(error='User not found. Please signup!'), 401)

        expires_in = timedelta(days=15)
        access_token = create_access_token(identity=user.email, expires_delta=expires_in)
        access_token_info = AccessToken(access_token=access_token, expires_in=str(expires_in), user_id=user.id)

        login_user(user, remember=request.json['email'])

        db.session.add(access_token_info)
        db.session.commit()
        return jsonify(access_token=access_token)

    except exc.SQLAlchemyError as e:
        return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
    except Exception as e:
        return make_response(jsonify(error_message=str(e)), 400)


@app.route('/logout')
def logout():
    logout_user()
    return make_response(jsonify(message=f'You are successfully logged out!'), 201)


@app.route('/news/sentiments', methods=['GET'])
@jwt_required()
def news_sentiment():
    try:
        df = DataProcessor.data_processing()
        news_sentiment_summary = SentimentAnalyzer.news_sentiment_summary(df)
        news_sentiment = SentimentAnalyzer.news_sentiment(df)
        return make_response(jsonify(status='ok', total_results=len(df),
                                         sentiment_percentage=news_sentiment_summary,
                                         detail_info=news_sentiment), 201)
    except exc.SQLAlchemyError as e:
        return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
    except Exception as e:
        return make_response(jsonify(error_message=str(e)), 400)


@app.route('/news/good-news', methods=['GET'])
@jwt_required()
def positive_news():
    try:
        df = DataProcessor.data_processing()
        news_sentiment = SentimentAnalyzer.positive(df)
        return make_response(jsonify(status='ok',
                                     total_results=len(news_sentiment),
                                     detail_info=news_sentiment), 201)
    except exc.SQLAlchemyError as e:
        return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
    except Exception as e:
        return make_response(jsonify(error_message=str(e)), 400)