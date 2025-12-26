import pytest
from Splity import create_app
from Splity.adapters.database import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False  # Makes testing forms much easier
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def authenticated_client(client):
    """Helper to register and log in a user for protected route tests."""
    client.post('/register', data={
        "name": "Test User", "username": "testuser", "email": "test@test.com",
        "password": "Password123", "password2": "Password123"
    })
    client.post('/login', data={"username": "testuser", "password": "Password123"})
    return client