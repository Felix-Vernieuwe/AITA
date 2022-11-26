import pandas
import pandas as pd

from schema import PostSchema
from whoosh import index
import tqdm
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

data = pandas.read_csv("aita_clean.csv")

index_dir = os.getenv("INDEX_DIR")
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

ix = index.create_in(index_dir, PostSchema)

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