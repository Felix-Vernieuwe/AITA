from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from api import Posts, Post

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(Posts, "/posts")
api.add_resource(Post, "/post")