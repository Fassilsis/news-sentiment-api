import operator

from flask import request, make_response, jsonify
from NewsApi.app import app, exception_handler
from NewsApi import models
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from NewsApi.errors import SchemaValidationError, EmailAlreadyExistsError, UserPermissionError, InternalServerError


class UserRegistration:
    def post(self):
        try:
            body = request.get_json()
            user = models.User(**body)
            user.hash_password()
            db.session.add(news_headline)
            db.session.commit()
            return make_response(jsonify(message= user), 200)
         # except FieldDoesNotExist:
         #     raise SchemaValidationError
         # except NotUniqueError:
         #     raise EmailAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class UserLogin():
     def post(self):
         try:
             body = request.get_json()
             user = models.User.objects.get(email=body.get('email'))
             authorized = user.check_password(body.get('password'))
             if not authorized:
                 raise UserPermissionError
             expiration_date = datetime.timedelta(days=30)
             access_token = create_access_token(identity=str(user.id), expires_delta=expiration_date)
             return make_response(jsonify(access_token='30-day-user-access-token',
                                          token_type='bearer',
                                          expires_in=f'{}'        }
         # except (UnauthorizedError, DoesNotExist):
         #     raise UnauthorizedError
         except Exception as e:
             raise InternalServerError