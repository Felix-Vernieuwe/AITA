import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import scoring
import os
from dotenv import load_dotenv

load_dotenv()

index_dir = os.getenv("INDEX_DIR")
ix = index.open_dir(index_dir)

with ix.searcher() as searcher:
    results = searcher.find("title", "cat")
    for result in results:
        print(f"Title: {result['title']} - URL: https://www.reddit.com/r/AmItheAsshole/comments/{result['url']}")

    # tf-idf
    # qp = QueryParser("body", schema=ix.schema)
    # q = qp.parse("cat")
    # with ix.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
    #     print(scoring.TF_IDF().scorer(searcher_tfidf, 'body', 'peanut').score(q.matcher(searcher_tfidf)))
    # with ix.searcher(weighting=scoring.BM25F()) as searcher_bm25f:
    #     print(scoring.BM25F().scorer(searcher_bm25f, 'body', 'peanut').score(q.matcher(searcher_bm25f)))