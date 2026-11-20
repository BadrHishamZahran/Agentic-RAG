from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.config import DOCUMENTS_PATH
from app.ingestion.loader import load_document, split_text
from app.vectorstore.store import add_chunks
from app.graph import run_agent

app = FastAPI(title="Agentic RAG API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class AskBody(BaseModel):
    question: str = Field(min_length=2, max_length=4000)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    name = Path(file.filename or "document.txt").name
    path = DOCUMENTS_PATH / name
    if path.suffix.lower() not in {".pdf", ".docx", ".txt"}:
        raise HTTPException(400, "Upload PDF, DOCX, or TXT files only.")
    path.write_bytes(await file.read())
    try:
        chunks = split_text(load_document(path))
        count = add_chunks(chunks, name)
        if not count:
            raise ValueError("No readable text found in this document.")
        return {"message": "Document indexed successfully", "filename": name, "chunks_added": count}
    except Exception as exc:
        raise HTTPException(400, str(exc))

@app.post("/ask")
def ask(body: AskBody):
    try:
        return run_agent(body.question)
    except Exception as exc:
        raise HTTPException(500, f"Agent execution failed: {exc}")
