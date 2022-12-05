import pandas
import pandas as pd
import whoosh.fields

from dotenv import load_dotenv
from schema import PostSchema
from whoosh import index
import tqdm
import datetime
import os
import praw

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="aita analyser",
    username=os.getenv("username"),
    password=os.getenv("password")
)

ix = index.open_dir("indexdir")

with ix.searcher() as searcher:
    results = searcher.find("title", "keep a cat")
    for result in results:
        submission = reddit.submission(result['url'])
        comments = set([comment.body for comment in submission.comments if comment.author and comment.author.name != "AutoModerator"])
        print(f"Title: {result['title']} - URL: https://www.reddit.com/r/AmItheAsshole/comments/{result['url']}")
        print(f"Num Comments: {len(comments)}")
        print(f"=======================================================")

