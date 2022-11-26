import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh import scoring

ix = index.open_dir("indexdir")

with ix.searcher() as searcher:
    results = searcher.find("title", "cat")
    for result in results:
        # Return frequency of term in document body
        # print(result["body"].frequency("cat"))
        a = searcher.search(QueryParser("body", ix.schema).parse("cat"))
        print(a.estimated_length())

    # tf-idf
    # qp = QueryParser("body", schema=ix.schema)
    # q = qp.parse("cat")
    # with ix.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
    #     print(scoring.TF_IDF().scorer(searcher_tfidf, 'body', 'peanut').score(q.matcher(searcher_tfidf)))
    # with ix.searcher(weighting=scoring.BM25F()) as searcher_bm25f:
    #     print(scoring.BM25F().scorer(searcher_bm25f, 'body', 'peanut').score(q.matcher(searcher_bm25f)))