# app/main.py
from __future__ import annotations
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.search.storage import Storage

DB_PATH = os.getenv("DB_PATH", "data/search.db")

app = FastAPI(title="BM25 Search")

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173", "https://your-frontend"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    # ensure schema exists
    s = Storage(DB_PATH)
    s.ensure_schema()
    s.close()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/search")
def search(q: str = Query(..., min_length=1), limit: int = 10, offset: int = 0):
    """
    VERY minimal BM25-ish search using your SQLite schema.
    Replace this with your real ranker if you already have one.
    """
    s = Storage(DB_PATH)
    try:
        # naive scoring: sum(tf * idf)  (you likely have a nicer function already)
        # idf = ln( (N - df + 0.5) / (df + 0.5) + 1 )
        rows = _rank_sql(s, q, limit, offset)
        return {"q": q, "count": len(rows), "results": rows}
    finally:
        s.close()

def _rank_sql(s: Storage, q: str, limit: int, offset: int):
    import math
    # tokenize like your indexer (import here to avoid circulars)
    from app.search.preprocess import normalize_and_tokenize
    toks = normalize_and_tokenize(q)
    if not toks:
        return []

    conn = s.conn
    cur = conn.execute("SELECT CAST(value AS INTEGER) FROM meta WHERE key='doc_count'")
    row = cur.fetchone()
    N = int(row[0]) if row and row[0] is not None else 0
    if N == 0:
        return []

    # Compute per-term idf
    idf = {}
    for t in toks:
        cur = conn.execute("SELECT df FROM terms WHERE term=?", (t,))
        row = cur.fetchone()
        df = int(row[0]) if row else 0
        # +1 for numerical stability
        idf[t] = math.log(((N - df + 0.5) / (df + 0.5)) + 1.0)

    # Aggregate scores per doc
    # (simple sum tf*idf; swap in your BM25 if you already implemented it)
    cur = conn.execute(
        f"""
        SELECT p.doc_id, d.url, d.title, d.text, SUM(p.tf * ?) as score
        FROM postings p
        JOIN documents d ON d.id = p.doc_id
        WHERE p.term IN ({",".join("?"*len(toks))})
        GROUP BY p.doc_id
        ORDER BY score DESC
        LIMIT ? OFFSET ?
        """,
        (1.0,) + tuple(toks) + (limit, offset)
    )
    results = []
    for doc_id, url, title, text, score in cur.fetchall():
        # tiny snippet
        snippet = (text[:300] + "…") if text and len(text) > 300 else (text or "")
        results.append({
            "doc_id": doc_id,
            "url": url,
            "title": title or "",
            "score": float(score or 0),
            "snippet": snippet
        })
    return results
