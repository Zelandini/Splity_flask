"""Initilise the App"""

from flask import Flask
# from flask_migrate import Migrate

from Splity.adapters.database import init_db
from config import Config
from flask_login import LoginManager


# Create login manager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialise database
    init_db(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "authentication.login"

    # Register blueprints
    from .home import routes
    app.register_blueprint(routes.home_blueprint)

    from .authentication import routes
    app.register_blueprint(routes.authentication_blueprint)

    return app

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from Splity.adapters.repository import UserRepository
    user_repo = UserRepository()
    return user_repo.get_by_id(int(user_id))