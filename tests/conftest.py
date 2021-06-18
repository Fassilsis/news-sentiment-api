import pytest
from NewsApi import create_app, db
from NewsApi.models.user_models import User, Role

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
        Role.insert_roles()
        user1 = User(username='user1', email='user1@dummyapp.com', password='password')
        user3 = User(username='user3', email='user3@dummyapp.com', password='password')
        admin = User(username='admin', email='admin@dummyapp.com', password='password')
        user1.add_to_db()
        user3.add_to_db()
        admin.add_to_db()

    yield client




