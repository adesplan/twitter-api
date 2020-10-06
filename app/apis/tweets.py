# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource, fields
from app.db import tweet_repository
from app.models import Tweet

api = Namespace('tweets')

tweet = api.model('Tweet', {
    'id': fields.Integer(readonly=True, description='The tweet unique identifier'),
    'text': fields.String(required=True, description='The tweet message'),
    'created_at': fields.DateTime(readonly=True, description='The creation date')
})


@api.route('/')
class TweetResource(Resource):

    @api.doc('get_tweet')
    @api.marshal_list_with(tweet)
    def get(self):
        return tweet_repository.tweets, 200

    @api.doc('create_tweet')
    @api.expect(tweet)
    @api.marshal_with(tweet, code=201)
    def post(self):
        """
        Create a new tweet
        """
        data = api.payload
        text = data['text']
        tweet_repository.add(Tweet(text))
        return "", 201



@api.route('/<int:id>')
@api.param('id', 'The tweet unique identifier')
@api.response(404, 'Tweet not found')
class TweetResource(Resource):
    @api.marshal_with(tweet, code=200)
    def get(self, id):
        tweet_to_return = tweet_repository.get(id)
        if tweet_to_return is None:
            api.abort(404)
        else:
            return tweet_to_return, 200
