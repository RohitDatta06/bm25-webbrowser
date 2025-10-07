import math
from typing import List, Dict, Tuple
from .preprocess import normalize_text
from .storage import get_db, get_meta


class BM25:
    def __init__(self, k1: float = 1.2, b: float = 0.75):
        self.k1 = k1
        self.b = b

    def idf(self, df: int, N: int) -> float:
        return math.log((N - df + 0.5) / (df + 0.5) + 1)


def search(query: str, k: int = 10) -> List[Tuple[int, float]]:
    q_terms = normalize_text(query)
    if not q_terms:
        return []
    with get_db() as con:
        cur = con.cursor()
        N = int(float(get_meta("N", "0")))
        avgdl = float(get_meta("avgdl", "0"))
        if N == 0:
            return []
        # fetch df for query terms
        q_marks = ",".join(["?"] * len(q_terms))
        cur.execute(f"SELECT term, df FROM df WHERE term IN ({q_marks})", q_terms)
        df_map = {t: d for t, d in cur.fetchall()}
        # fetch postings for query terms
        cur.execute(f"SELECT term, doc_id, tf FROM postings WHERE term IN ({q_marks})", q_terms)
        post_rows = cur.fetchall()
        # fetch doc lengths for involved docs
        doc_ids = list({d for _, d, _ in post_rows})
        if not doc_ids:
            return []
        id_marks = ",".join(["?"] * len(doc_ids))
        cur.execute(f"SELECT id, length FROM docs WHERE id IN ({id_marks})", doc_ids)
        dl_map = {i: l for i, l in cur.fetchall()}

    bm25 = BM25()
    scores: Dict[int, float] = {}
    for term, doc_id, tf in post_rows:
        df = df_map.get(term, 0)
        idf = bm25.idf(df, N)
        dl = dl_map.get(doc_id, 0) or 1
        denom = tf + bm25.k1 * (1 - bm25.b + bm25.b * (dl / (avgdl or 1)))
        s = idf * ((tf * (bm25.k1 + 1)) / denom)
        scores[doc_id] = scores.get(doc_id, 0.0) + s

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]