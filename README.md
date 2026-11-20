# Agentic RAG

An Agentic Retrieval-Augmented Generation system. The agent plans a response, selects tools, retrieves uploaded documents, optionally searches the web, performs calculations, and synthesizes an answer with available sources.

## Features
- Local LLM with Ollama (`qwen2.5:3b`)
- LangGraph agent workflow: Planner -> Tool Executor -> Answer Generator
- PDF, DOCX, and TXT ingestion
- Sentence Transformers embeddings and ChromaDB vector search
- DuckDuckGo web search (no paid API key)
- Safe arithmetic calculator
- FastAPI backend and React + Vite frontend
- Python 3.10+; no GPU or paid API required

## Requirements
- Python 3.10+
- Node.js 20+
- Ollama
- 16 GB RAM recommended (works with CPU inference; speed depends on hardware)

## 1. Ollama
Install from https://ollama.com/download, then run:
```cmd
ollama pull qwen2.5:3b
ollama run qwen2.5:3b
```
Type `/bye` to exit the test. Keep Ollama running while using the app.

## 2. Backend setup (Windows CMD)
From the project root:
```cmd
cd backend
py -3.10 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
Python 3.11 or newer can also be used by replacing `py -3.10` with the installed version.

## 3. Start backend
From `backend` with `.venv` activated:
```cmd
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000  
Swagger: http://127.0.0.1:8000/docs

## 4. Start frontend
Open a second CMD:
```cmd
cd frontend
npm install
npm run dev
```
Open the URL printed by Vite, usually http://localhost:5173.

## 5. How to use
1. Upload PDF, DOCX, or TXT files.
2. Wait for indexing to finish.
3. Ask a question.
4. Inspect selected tools, agent activity, and sources.

Example questions:
- Summarize the main ideas in my uploaded documents.
- Compare two concepts discussed in my documents.
- Search the web for recent information about RAG and compare it with my notes.
- Calculate 125 * 18 and explain the result.

## Agent workflow
- **Planner:** chooses useful tools for the user's request.
- **Tool Executor:** runs selected tools sequentially (maximum three).
- **Answer Generator:** combines the tool outputs and reports available sources.

Available tools: `document_search`, `web_search`, and `calculator`. The planner does not need to call every tool for every question.

## Project structure
```text
Agentic-RAG/
├── README.md
├── .gitignore
├── backend/
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── graph.py
│   │   ├── ingestion/loader.py
│   │   ├── vectorstore/store.py
│   │   ├── agent/planner.py
│   │   └── tools/
│   │       ├── document_search.py
│   │       ├── web_search.py
│   │       └── calculator.py
│   └── data/documents/.gitkeep
└── frontend/
    ├── package.json
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        └── styles.css
```

## Configuration
Edit `backend/.env`:
- `OLLAMA_BASE_URL`: default `http://localhost:11434`
- `OLLAMA_MODEL`: default `qwen2.5:3b`
- `EMBEDDING_MODEL`: default `sentence-transformers/all-MiniLM-L6-v2`
- `CHROMA_PATH`: local vector database path
- `TOP_K`: number of retrieved chunks

The embedding model is downloaded on first use. Document retrieval works locally. Web search needs internet access and may occasionally be rate-limited.

## GitHub upload
Create an empty GitHub repository, then run from the project root:
```cmd
git init
git add .
git commit -m "Initial commit: Agentic RAG"
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Agentic-RAG.git
git push -u origin main
```
Replace the username and URL with your own. Do not upload `.env`, virtual environments, `node_modules`, vector database files, private documents, or model weights; `.gitignore` excludes them.