from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_apiexceptions import JSONExceptionHandler
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config["JWT_SECRET_KEY"] = "1234567890"  # Change this!
app.config["SECRET_KEY"] = "1234567890"  # Change this!

login = LoginManager(app)
login.login_view = 'login'


db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)


exception_handler = JSONExceptionHandler(app)

from NewsApi import routes
