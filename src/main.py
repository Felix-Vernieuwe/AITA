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

data = pandas.read_csv("aita_clean.csv")


if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = index.create_in('indexdir', PostSchema)

writer = ix.writer()

# Set row timestamp as int type
data['timestamp'] = pd.to_datetime(data['timestamp'], unit="s")
data['timestamp'] = pd.Series(data['timestamp'].dt.to_pydatetime(), dtype=object)
data = data.fillna("0")
data['timestamp'] = pd.Series(data['timestamp'].dt.to_pydatetime(), dtype=object)

loading_bar = tqdm.tqdm(len(data))
for index, row in data.iterrows():
    writer.add_document(url=row["id"], timestamp=row["timestamp"], title=row["title"], body=row["body"], edited=row["edited"],
                        verdict=row["verdict"], score=row["score"], num_comments=row["num_comments"])
    loading_bar.update(1)
writer.commit()

# data = pandas.read_csv("aita_clean.csv")
# for index, row in data.iterrows():
#     print("*" * 100)
#     print("ID")
#     print(row["id"])
#     print("TITLE")
#     print(row["title"])
#     print("BODY")
#     print(row["body"])
#     print()
#     if index == 20:
#         break