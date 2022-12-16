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

from summary import lexrank_summary

with ix.searcher() as searcher:
    results = searcher.find("title", "mentally handicap sister")
    for result in results:
        submission = reddit.submission(result['url'])
        
        yta = set()
        nta = set()
        for comment in submission.comments:
            if not isinstance(comment, praw.models.Comment) or not comment.author or comment.author.name == "AutoModerator":
                continue
            if any(yta in comment.body for yta in ("YTA", "ESH")):
                yta |= {comment.body}
            if any(nta in comment.body for nta in ("NTA", "NAH")):
                nta |= {comment.body} 
        
        print(f"Title: {result['title']} - URL: https://www.reddit.com/r/AmItheAsshole/comments/{result['url']}")
        print("\nContent: " + " ".join([f"{sentence}" for sentence in lexrank_summary(submission.selftext)]))
        print(f"\nYTA ({len(yta)}): " + " ".join([f"{sentence}" for sentence in lexrank_summary(*yta)]))
        print(f"\nNTA ({len(nta)}): " + " ".join([f"{sentence}" for sentence in lexrank_summary(*nta)]))
        print(f"\nNum Comments: {len(yta) + len(nta)}")
        print(f"=======================================================")

