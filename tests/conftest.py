import pytest
from NewsApi import create_app, db
from NewsApi.models.user_models import User

app = create_app()


@pytest.fixture
def client():
    """
    Create a temporary db with some data in it for using in the tests.
    """
    app.config["TESTING"] = True
    app.testing = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    client = app.test_client()
    with app.app_context():
        db.drop_all()
        db.create_all()
        user1 = User(username='user1', email='user1@dummyapp.com', password='password', role_name='user')
        user2 = User(username='user2', email='user2@dummyapp.com', password='password', role_name='user')
        user3 = User(username='user3', email='user3@dummyapp.com', password='password', role_name='user')
        admin = User(username='admin', email='admin@dummyapp.com', password='password', role_name='admin')
        db.session.add(user1)
        db.session.add(user3)
        db.session.add(admin)
        db.session.commit()
    yield client




