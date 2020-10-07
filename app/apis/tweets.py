# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource, fields
from app import db
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
        return db.session.query(Tweet).all(), 200

    @api.doc('create_tweet')
    @api.expect(tweet)
    @api.marshal_with(tweet, code=201)
    def post(self):
        """
        Create a new tweet
        """
        tweet_to_add = Tweet()
        tweet_to_add.text = api.payload['text']
        db.session.add(tweet_to_add)
        db.session.commit()
        return tweet_to_add, 201


@api.route('/<int:id>')
@api.param('id', 'The tweet unique identifier')
@api.response(404, 'Tweet not found')
class TweetResource(Resource):
    @api.doc('get_tweet')
    @api.marshal_with(tweet, code=200)
    def get(self, id):
        tweet_to_return = Tweet.query.filter_by(id=id).first()
        if tweet_to_return is None:
            api.abort(404)
        return tweet_to_return, 200

    @api.doc('update_tweet')
    @api.expect(tweet)
    @api.marshal_with(tweet, code=200)
    def patch(self, id):
        tweet_to_patch = Tweet.query.filter_by(id=id).first()
        if tweet_to_patch is None:
            api.abort(404)
        data = api.payload
        tweet_to_patch.text = data['text']
        db.session.commit()
        return tweet_to_patch, 200

    @api.doc('delete_tweet')
    @api.marshal_with(tweet, code=204)
    def delete(self, id):
        tweet_to_delete = db.session.query(Tweet).get(id)
        if tweet_to_delete is None:
            api.abort(404)
        db.session.delete(tweet_to_delete)
        db.session.commit()
        return "", 204
