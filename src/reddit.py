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

submission = reddit.submission("1ytxov")
print(submission.title)
comments = submission.comments
for comment in comments:
    print("*" * 100)
    print(comment.body_html)
    print(comment.banned_by, comment.author)