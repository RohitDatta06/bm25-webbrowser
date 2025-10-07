# BM25 Search Engine

Access site - (https://bm25-frontend.onrender.com/)

A lightweight full-stack search engine that indexes and ranks real web pages using the **BM25 algorithm**.  
Built with **FastAPI**, **SQLite**, and a **React + TypeScript (Vite)** frontend.  
The system can crawl websites or ingest data from **Common Crawl WET** files, tokenize and index documents, and serve ranked search results through a clean web interface.

---

## 🚀 Features

### 🔍 Core Search
- **BM25 ranking** implementation with per-term TF-IDF weighting.
- **Tokenization and normalization** pipeline for web text.
- **Common Crawl ingestion** via streaming WET/WARC files.
- **SQLite-based inverted index** — lightweight, portable, no dependencies.
- **FastAPI REST API** with `/search` endpoint for ranked queries.

### 🖥️ Frontend
- Responsive **React + TypeScript** interface built with **Vite**.
- Query box, ranked result list, and dynamic loading.
- Clean minimalist design using **Tailwind CSS** and **shadcn/ui** components.

### ⚙️ Backend
- **FastAPI** for REST + CORS support.
- **Uvicorn** ASGI server for deployment.
- Efficient batch indexing with `Storage` abstraction.
- Schema auto-creation, incremental indexing, and metadata caching.

### 🗂️ Data Ingestion
- Built-in `cli.py` with:
  - `ingest-cc` → stream & index Common Crawl WET files.
  - `ensure-schema` → auto-create tables.
- Uses the **warcio** library for reading large compressed WET files.
- Configurable limit for lightweight or full-scale indexing.

### ☁️ Deployment
- Fully deployable on **Render (Free tier)** using `render.yaml` blueprint:
  - `bm25-api` → FastAPI backend
  - `bm25-frontend` → Vite static frontend
- Ships with a small pre-built SQLite database for instant demo results.

---

## 🧱 Technologies Used

| Layer | Technologies |
|-------|---------------|
| **Frontend** | React • TypeScript • Vite • Tailwind CSS • shadcn/ui |
| **Backend** | FastAPI • Uvicorn • SQLite • Python 3.12 |
| **Indexing & NLP** | BM25 • Tokenization • Regex normalization • warcio (Common Crawl) |
| **Infrastructure** | Render (Free Plan) • GitHub • curl • gzip |
| **Dev Tools** | pip • npm • virtualenv • sqlite3 • REST APIs • JSON |

---


