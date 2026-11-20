import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parents[1]
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", str(BASE_DIR / "data" / "chroma")))
DOCUMENTS_PATH = Path(os.getenv("DOCUMENTS_PATH", str(BASE_DIR / "data" / "documents")))
TOP_K = int(os.getenv("TOP_K", "5"))
CHROMA_PATH.mkdir(parents=True, exist_ok=True)
DOCUMENTS_PATH.mkdir(parents=True, exist_ok=True)
