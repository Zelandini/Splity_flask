"""Initilise the App"""

from flask import Flask
# from flask_migrate import Migrate

from Splity.adapters.database import init_db
from config import Config
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object(Config)
# from flask_sqlalchemy import SQLAlchemy
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # migrate = Migrate(app, db)
    init_db(app)

    login_manager.init_app(app)
    login_manager.login_view = "authentication_blueprint.login"

    from .home import routes
    app.register_blueprint(routes.home_blueprint)

    from .authentication import routes
    app.register_blueprint(routes.authentication_blueprint)

    return app

@login_manager.user_loader
def load_user(user_id):
    from Splity.adapters.repository import UserRepository
    user_repo = UserRepository()
    return user_repo.get_by_id(int(user_id))