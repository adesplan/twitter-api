# app/__init__.py
# pylint: disable=missing-docstring

from flask import Flask
from flask_restx import Api
from app.db import tweet_repository
from app.models import Tweet
tweet_repository.add(Tweet("a first tweet"))
tweet_repository.add(Tweet("a second tweet"))


def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return "Hello from a Blueprint! Goodbye World!"

    from app.apis.tweets import api as tweets
    api = Api()
    api.add_namespace(tweets)
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False
    return app
