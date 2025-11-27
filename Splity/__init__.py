"""Initilise the App"""

from pathlib import Path

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    from .home import routes
    app.register_blueprint(routes.home_blueprint)

    return app