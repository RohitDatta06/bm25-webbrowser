# app/search/storage.py
from __future__ import annotations
import sqlite3
from collections import Counter
from typing import Any, Dict, List


class Storage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")

    def ensure_schema(self) -> None:
        cur = self.conn.cursor()

        # Basic doc store
        cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id      INTEGER PRIMARY KEY,
            url     TEXT UNIQUE,
            title   TEXT,
            text    TEXT,
            length  INTEGER
        );
        """)

        # Term dictionary (df = document frequency)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS terms (
            term TEXT PRIMARY KEY,
            df   INTEGER NOT NULL DEFAULT 0
        );
        """)

        # Inverted index postings (tf = term frequency per doc)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS postings (
            term    TEXT NOT NULL,
            doc_id  INTEGER NOT NULL,
            tf      INTEGER NOT NULL,
            PRIMARY KEY (term, doc_id),
            FOREIGN KEY (doc_id) REFERENCES documents(id) ON DELETE CASCADE
        );
        """)

        # Misc metadata (e.g., avgdl, doc_count)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT
        );
        """)

        cur.execute("CREATE INDEX IF NOT EXISTS idx_postings_term ON postings(term);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_postings_doc  ON postings(doc_id);")
        self.conn.commit()

    def upsert_batch(self, batch: List[Dict[str, Any]]) -> None:
        """
        batch item shape: {"url": str, "title": str, "text": str, "tokens": List[str]}
        """
        cur = self.conn.cursor()

        for doc in batch:
            url   = doc.get("url", "")
            title = doc.get("title", "")
            text  = doc.get("text", "")
            toks  = doc.get("tokens", [])

            # Insert or update the document row
            cur.execute(
                "INSERT OR IGNORE INTO documents(url, title, text, length) VALUES (?,?,?,NULL)",
                (url, title, text),
            )
            cur.execute(
                "UPDATE documents SET title = ?, text = ? WHERE url = ?",
                (title, text, url),
            )
            # Get doc_id
            cur.execute("SELECT id FROM documents WHERE url = ?", (url,))
            row = cur.fetchone()
            if not row:
                # Shouldn't happen, but be defensive
                continue
            doc_id = row[0]

            # Store doc length
            length = len(toks)
            cur.execute("UPDATE documents SET length = ? WHERE id = ?", (length, doc_id))

            # Upsert postings + ensure term exists
            counts = Counter(toks)
            for term, tf in counts.items():
                # Ensure term exists in dictionary
                cur.execute("INSERT OR IGNORE INTO terms(term, df) VALUES (?, 0)", (term,))
                # Upsert posting
                cur.execute(
                    """
                    INSERT INTO postings(term, doc_id, tf) VALUES (?,?,?)
                    ON CONFLICT(term, doc_id) DO UPDATE SET tf = excluded.tf
                    """,
                    (term, doc_id, tf),
                )

        # Recompute df (document frequency) for all terms touched
        cur.execute("""
            UPDATE terms
            SET df = (SELECT COUNT(*) FROM postings p WHERE p.term = terms.term)
        """)

        # Recompute metadata
        cur.execute("REPLACE INTO meta(key, value) VALUES('doc_count', (SELECT COUNT(*) FROM documents))")
        cur.execute("REPLACE INTO meta(key, value) VALUES('avgdl',     (SELECT COALESCE(AVG(length), 0) FROM documents))")

        self.conn.commit()

    def close(self) -> None:
        self.conn.close()


__all__ = ["Storage"]
