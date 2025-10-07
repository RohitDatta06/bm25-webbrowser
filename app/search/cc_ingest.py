# app/search/cc_ingest.py
from __future__ import annotations
from typing import Iterator, Tuple, Optional
from warcio.archiveiterator import ArchiveIterator
import gzip
import io
import os
import sys

def _iter_records_from_stream(stream: io.BufferedReader) -> Iterator[Tuple[str, Optional[str], str]]:
    """
    Yields (url, title, text) triples from a WET or WARC->WET 'conversion' stream.
    Title may be None (WET often doesn’t include HTML <title/> reliably).
    """
    for rec in ArchiveIterator(stream):
        # WET uses rec_type == 'conversion' with plain text payload
        if rec.rec_type != 'conversion':
            continue
        url = rec.rec_headers.get_header('WARC-Target-URI') or ""
        raw = rec.content_stream().read()
        # Content is plaintext in WET; decode forgivingly
        text = raw.decode('utf-8', errors='ignore')
        if url and text.strip():
            yield (url, None, text)

def iter_wet(path_or_gz: str) -> Iterator[Tuple[str, Optional[str], str]]:
    """
    Open a .wet or .wet.gz and yield (url, title, text).
    """
    # Accept plain .wet, gzipped .wet.gz, or stdin (“-”)
    if path_or_gz == "-":
        # if stdin is gz, warcio can still parse; try gzip first
        try:
            with gzip.GzipFile(fileobj=sys.stdin.buffer) as gz:
                yield from _iter_records_from_stream(gz)  # type: ignore
            return
        except OSError:
            # not gzipped
            yield from _iter_records_from_stream(sys.stdin.buffer)  # type: ignore
            return

    if path_or_gz.endswith(".gz"):
        with gzip.open(path_or_gz, "rb") as f:
            yield from _iter_records_from_stream(f)  # type: ignore
    else:
        # .wet file (already decompressed)
        with open(path_or_gz, "rb") as f:
            yield from _iter_records_from_stream(f)  # type: ignore
