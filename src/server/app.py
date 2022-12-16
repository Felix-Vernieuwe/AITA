from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from api import Posts, Post, Sentiment, Summary

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(Posts, "/posts")
api.add_resource(Post, "/post")
api.add_resource(Sentiment, "/sentiment")
api.add_resource(Summary, "/summary")