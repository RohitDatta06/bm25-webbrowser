
from __future__ import annotations
import html
import re
from typing import List
import re
from typing import List

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    from nltk.tokenize import wordpunct_tokenize
except Exception:
    nltk = None

_STOP = None
_STEM = None


def _ensure_nltk():
    global _STOP, _STEM
    if nltk is None:
        raise RuntimeError("NLTK not installed; check requirements.txt")
    try:
        stopwords.words("english")
    except LookupError:
        import nltk as _n
        _n.download("stopwords")
    try:
        wordpunct_tokenize("test")
    except LookupError:
        import nltk as _n
        _n.download("punkt")
    _STOP = set(stopwords.words("english"))
    _STEM = PorterStemmer()


def normalize_text(text: str) -> List[str]:
    if _STOP is None or _STEM is None:
        _ensure_nltk()
    text = re.sub(r"\s+", " ", text).lower()
    toks = [t for t in wordpunct_tokenize(text) if re.search(r"[a-z0-9]", t)]
    toks = [t for t in toks if t not in _STOP and len(t) > 2]
    toks = [_STEM.stem(t) for t in toks]
    return toks

_STOP = {
    "a","an","and","are","as","at","be","by","for","from","has","he","in","is",
    "it","its","of","on","that","the","to","was","were","will","with","this",
    "but","or","if","then","than","so","not","we","you","they","their","them",
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")

def normalize_and_tokenize(text: str) -> List[str]:
    """
    Lowercase, HTML-unescape, strip non-alphanum, split on [a-z0-9]+,
    drop short/stopword tokens.
    """
    if not text:
        return []
    t = html.unescape(text).lower()
    toks = _TOKEN_RE.findall(t)
    # filter: length >= 2, not purely digits, not in stopwords
    out = []
    for w in toks:
        if len(w) < 2:
            continue
        if w.isdigit():
            continue
        if w in _STOP:
            continue
        out.append(w)
    return out

__all__ = ["normalize_and_tokenize"]
