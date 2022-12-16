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

index_dir = os.getenv("INDEX_DIR")
ix = index.open_dir(index_dir)

from summary import lexrank_summary, bert_summary

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
        for summary, name in zip([lexrank_summary, bert_summary], ["Lexrank", "BERT"]):
            print(f"Summary using {name}")
            print(f"\nContent: {summary(submission.selftext)}")
            print(f"\nYTA ({len(yta)}): {summary(*yta)}")
            print(f"\nNTA ({len(nta)}): {summary(*nta)}")
            print(f"\nNum Comments: {len(yta) + len(nta)}")
            print(f"=======================================================")
