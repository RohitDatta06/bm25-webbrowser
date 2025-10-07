# app/cli.py (append this subcommand to your argparse/click)
import argparse
from pathlib import Path
from .search.cc_ingest import iter_wet
from .search.indexer import index_documents

def main():
    parser = argparse.ArgumentParser(description="BM25 tools")
    sub = parser.add_subparsers(dest="cmd")

    cc = sub.add_parser("ingest-cc", help="Ingest Common Crawl WET files into the index")
    cc.add_argument("--db", default="data/search.db")
    cc.add_argument("--wet", nargs="+", required=True, help="Paths to .wet or .wet.gz files (or '-')")

    args = parser.parse_args()
    if args.cmd == "ingest-cc":
        # chain all files
        def docs():
            for p in args.wet:
                yield from iter_wet(p)
        Path(args.db).parent.mkdir(parents=True, exist_ok=True)
        index_documents(args.db, docs())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
