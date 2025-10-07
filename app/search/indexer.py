# app/search/indexer.py  (add this helper; keep your existing functions)
from typing import Iterator, Optional, Tuple
from .preprocess import normalize_and_tokenize
from .storage import Storage

# Expect docs as (url, title_or_None, text)
Doc = Tuple[str, Optional[str], str]

def index_documents(db_path: str, docs: Iterator[Doc], batch_size: int = 500):
    """
    Stream-in indexer: tokenizes and writes to SQLite in batches.
    """
    store = Storage(db_path)
    store.ensure_schema()

    batch = []
    for url, title, text in docs:
        tokens = normalize_and_tokenize(text)
        batch.append({"url": url, "title": title or "", "text": text, "tokens": tokens})
        if len(batch) >= batch_size:
            store.upsert_batch(batch)
            batch.clear()
    if batch:
        store.upsert_batch(batch)
