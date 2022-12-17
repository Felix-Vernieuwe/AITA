import os
import json
import pandas as pd

from whoosh import scoring
import whoosh.index as index
from whoosh.qparser import MultifieldParser, OrGroup

from flask import request
from flask_restful import Resource

import praw
from dotenv import load_dotenv

from classifiers.doc2vec_classifier import Doc2VecClassifier
from classifiers.multinominal_bayes_classifier import MultinomialBayesClassifier
from classifiers.bert_classifier import BertClassifier
from classifiers.classifier import preprocess_dataset

from conversions import html
from summary import lexrank_summary, bert_summary

load_dotenv()

df = pd.read_csv("../../dataset/aita_clean.csv")
training_set, test_set = preprocess_dataset(df)

bert_classifier = BertClassifier()
mnb_classifier = MultinomialBayesClassifier()
doc2vec_classifier = Doc2VecClassifier()

ALWAYS_TRAIN = False

if ALWAYS_TRAIN:
    bert_classifier.train(training_set)
    mnb_classifier.train(training_set)
    doc2vec_classifier.train(training_set)
else:
    try:
        print("Loading BERT data from disk...")
        bert_classifier.load_model()
    except Exception as e:
        print(e)
        print("Could not find data for BERT. Training model with provided data...")
        bert_classifier.train(training_set)
        bert_classifier.save_model()

    try:
        print("Loading MNB data from disk...")
        mnb_classifier.load_model()
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print("Could not find data for MNB. Training model with provided data...")
            mnb_classifier.train(training_set)
            mnb_classifier.save_model()
        else:
            raise e

    try:
        print("Loading Doc2Vec data from disk...")
        doc2vec_classifier.load_model()
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print("Could not find data for Doc2Vec. Training model with provided data...")
            doc2vec_classifier.train(training_set)
            doc2vec_classifier.save_model()
        else:
            raise e

# bert_classifier.print_metrics(test_set)
# mnb_classifier.print_metrics(test_set)

try:
    import nltk

    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class Posts(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        index_dir = os.getenv("INDEX_DIR")
        self.index = index.open_dir(index_dir)

    def get(self):
        query_string = request.args["query"]
        fields = request.args["filters"].split(",")
        query_parser = MultifieldParser(fields, schema=self.index.schema, group=OrGroup)
        query = query_parser.parse(query_string)
        with self.index.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
            jsonify = lambda result: {"url": result["url"], "title": result["title"], "verdict": result["verdict"],
                                      "timestamp": result["timestamp"].isoformat()}
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

        suitable = lambda comment: type(
            comment) == praw.models.Comment and comment.author and comment.author.name != "AutoModerator"
        comments = [html(comment.body) for comment in submission.comments if suitable(comment)]
        return {"comments": comments, "body": html(submission.selftext), "title": submission.title}, 200


class Sentiment(Resource):
    def __init__(self):
        self.classifiers = {"BERT": bert_classifier, "MNB": mnb_classifier, "Doc2Vec": doc2vec_classifier}

    def get(self):
        classifier = self.classifiers[request.args["method"]]
        nta, certainty = classifier.classify(request.args["body"])
        return {"nta": bool(nta), "certainty": certainty}, 200


class Summary(Resource):
    def __init__(self):
        self.summarizers = {"LexRank": lexrank_summary, "BERT": bert_summary}

        self.reddit = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent="aita analyser",
            username=os.getenv("username"),
            password=os.getenv("password")
        )

    def get(self):
        summarize = self.summarizers[request.args["method"]]
        # if "url" not in request.args:
        #     return {"summary": summarize(request.args["body"])}, 200

        submission = self.reddit.submission(request.args["url"])

        yta = set()
        nta = set()
        for comment in submission.comments:
            if not isinstance(comment,
                              praw.models.Comment) or not comment.author or comment.author.name == "AutoModerator":
                continue
            if any(yta in comment.body for yta in ("YTA", "ESH")):
                yta |= {comment.body}
            if any(nta in comment.body for nta in ("NTA", "NAH")):
                nta |= {comment.body}

        return {"post": summarize(submission.selftext), "yta": summarize(*yta), "yta_count": len(yta),
                "nta": summarize(*nta), "nta_count": len(nta)}, 200
