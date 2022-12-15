import os

import praw
from bs4 import BeautifulSoup
from dotenv import load_dotenv

import conversions

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="aita analyser",
    username=os.getenv("username"),
    password=os.getenv("password")
)

submission = reddit.submission("1ytxov")
print(submission.title)
comments = submission.comments
for comment in comments:
    if comment.body != "[deleted]":
        print("*" * 100)
        print(conversions.plain_text(comment.body_html))