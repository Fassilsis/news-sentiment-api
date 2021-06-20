from datetime import datetime
from NewsApi import db, login_manager
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role_name = db.Column(db.String, db.ForeignKey('roles.name'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == "admin@dummyapp.com":
                self.role = Role.query.filter_by(name='admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {'created_on': self.created_on,
                'role_name': self.role_name,
                'email': self.email,
                'user_id': self.id,
                'user_name': self.username}

    @classmethod
    def filter_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def is_administrator(self):
        return self.role_name == 'admin'

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    default = db.Column(db.Boolean, default=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    @staticmethod
    def insert_roles():
        roles = {'user', 'admin'}
        default_role = 'user'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name