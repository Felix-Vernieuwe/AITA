import os
import json

from whoosh import scoring
import whoosh.index as index
from whoosh.qparser import MultifieldParser

from flask import request
from flask_restful import Resource

import praw
from dotenv import load_dotenv

from src.conversions import html

load_dotenv()

class Posts(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        index_dir = os.getenv("INDEX_DIR")
        self.index = index.open_dir(index_dir)

    def get(self):
        query_string = request.args["query"]
        fields = request.args["filters"].split(",")
        query_parser = MultifieldParser(fields, schema=self.index.schema)
        query = query_parser.parse(query_string)
        with self.index.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
            jsonify = lambda result: {"url": result["url"], "title": result["title"]}
            return {"posts": [jsonify(result) for result in searcher_tfidf.search(query, limit=20)]}, 200

class Post(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reddit = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent="aita analyser",
            username=os.getenv("username"),
            password=os.getenv("password")
        )

    def get(self):
        submission = self.reddit.submission(request.args["url"])
        
        suitable = lambda comment: type(comment) == praw.models.Comment and comment.author and comment.author.name != "AutoModerator"
        comments = [html(comment.body) for comment in submission.comments if suitable(comment)]
        return {"comments": comments, "body": html(submission.selftext), "title": submission.title}, 200

class Sentiment(Resource):
    def get(self):
        body = request.args["body"]
        return {"nta": False, "certainty": 82.3}, 200