from datetime import timedelta
from NewsApi.models.user_models import User, Role
from flask import jsonify, request, make_response, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from sqlalchemy import exc
from NewsApi import db


users = Blueprint('users', __name__)


@users.route('/users')
@users.route('/users/home')
def home():
    return 'Api for users'


@users.before_request
def add_roles():
    Role.insert_roles()


@users.route('/users/register', methods=['POST'])
def register():
    try:
        body = request.get_json()
        if User.filter_by_username(body['username']):
            return make_response(jsonify(message='User account with that username already exists.'), 400)

        new_user = User(**body)
        if len(body.get("password")) >= 8:
            new_user.hash_password()
        else:
            return make_response(jsonify(message='Password should be at least 8 characters'), 400)

        new_user.add_to_db()
        return make_response(jsonify(message=f'User account successfully created!'), 201)

    except exc.SQLAlchemyError as e:
        return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
    except Exception as e:
        return make_response(jsonify(error_message=str(e)), 400)


@users.route('/users/login', methods=['POST'])
def login():
    try:
        user = User.query.filter_by(username=request.json['username']).first()

        if user:
            authorized = user.check_password(password=request.json['password'])
            if authorized:
                login_user(user, remember=True)
                expires_in = timedelta(days=15)
                access_token = create_access_token(identity=user.email, expires_delta=expires_in)
                return jsonify(message='Logged in successfully', access_token=access_token)
            else:
                return make_response(jsonify(error='Login Unsuccessful. Please check password'), 401)

        else:
            return make_response(jsonify(error='User not found. Please enter a valid username or register!'), 404)

    except exc.SQLAlchemyError as e:
        return make_response(jsonify(SQLAlchemy_error_message=str(e)), 400)
    except Exception as e:
        return make_response(jsonify(error_message=str(e)), 400)


@users.route('/users/logout')
@login_required
def logout():
    logout_user()
    return make_response(jsonify(message='You are successfully logged out!'), 201)


@users.route('/users/management', methods=['GET', 'PUT', 'DELETE'])
@login_required
def manage_user_info():
    if not current_user:
        return make_response(jsonify(error_message='You need to sign in as administrator to view this resource.'), 403)

    if not current_user.is_administrator():
        return make_response(jsonify(error_message='You are not authorised to view this resource.'), 403)

    body = request.get_json()
    target_user = User.filter_by_username(body['username'])
    if not target_user:
        return make_response(jsonify(error_message='User not found.'), 404)

    if request.method == 'GET':
        return make_response(jsonify(users=target_user.serialize()), 200)

    elif request.method == 'PUT':
        target_user.username = body['new_username']
        db.session.commit()
        return make_response(jsonify(message='User updated.'), 201)

    elif request.method == 'DELETE':
        target_user.remove_from_db()
        return make_response(jsonify(message='User deleted.'), 201)


@users.route('/users/search', methods=['GET'])
@login_required
def search_all():
    if not current_user.is_administrator():
        return make_response(jsonify(error_message='You are not authorised to view this resource.'), 403)

    else:
        search_result = list(map(lambda user: user.serialize(), User.query.all()))
        total_users = User.query.count()
        return make_response(jsonify(users=search_result, total_users=total_users), 200)
