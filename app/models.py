# app/models.py
# pylint: disable=missing-docstring

from datetime import datetime
from app import db


class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_username = db.Column(db.String, db.ForeignKey('users.username'))

    def __repr__(self):
        return f"<Tweet #{self.id}>"


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(280), primary_key=True)
    email = db.Column(db.String(280))
    api_key = db.Column(db.String(280))
    tweets = db.relationship("Tweet")

    def __repr__(self):
        return f"<User #{self.user}>"
