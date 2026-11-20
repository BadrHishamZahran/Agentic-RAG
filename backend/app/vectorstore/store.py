from functools import lru_cache
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K

@lru_cache(maxsize=1)
def embedder():
    return SentenceTransformer(EMBEDDING_MODEL)

@lru_cache(maxsize=1)
def collection():
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_or_create_collection("agentic_rag", metadata={"hnsw:space": "cosine"})

def add_chunks(chunks: list[str], filename: str) -> int:
    if not chunks:
        return 0
    col = collection()
    offset = col.count()
    vectors = embedder().encode(chunks, normalize_embeddings=True).tolist()
    col.add(
        ids=[f"chunk_{offset+i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=vectors,
        metadatas=[{"source": filename} for _ in chunks]
    )
    return len(chunks)

def search_documents(query: str) -> list[dict]:
    col = collection()
    if col.count() == 0:
        return []
    vector = embedder().encode([query], normalize_embeddings=True).tolist()
    result = col.query(query_embeddings=vector, n_results=min(TOP_K, col.count()))
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    return [{"text": d, "source": m.get("source", "Unknown")} for d, m in zip(docs, metas)]
