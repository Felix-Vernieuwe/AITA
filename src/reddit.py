from dotenv import load_dotenv
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

aita = reddit.subreddit("AmITheAsshole")

for submission in reddit.subreddit("AmITheAsshole").hot(limit=10):
    print(submission.title)