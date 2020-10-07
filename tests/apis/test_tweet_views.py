# tests/apis/test_tweet_views.py

from flask_testing import TestCase
from app import create_app


class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app
