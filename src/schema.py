from whoosh.fields import SchemaClass, TEXT, BOOLEAN, ID, DATETIME, KEYWORD, NUMERIC

class PostSchema(SchemaClass):
    url = ID(stored=True)
    timestamp = DATETIME(stored=True)
    title = TEXT(stored=True)
    body = TEXT
    edited = BOOLEAN
    verdict = KEYWORD(stored=True, commas=True)
    score = NUMERIC
    num_comments = NUMERIC
    is_asshole = BOOLEAN