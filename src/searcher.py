import whoosh.index as index

ix = index.open_dir("indexdir")

with ix.searcher() as searcher:
    results = searcher.find("title", "cat")
    for result in results:
        print(result)
        