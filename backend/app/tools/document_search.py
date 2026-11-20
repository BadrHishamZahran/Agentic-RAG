from app.vectorstore.store import search_documents

def document_search(query: str) -> dict:
    results = search_documents(query)
    return {"tool": "document_search", "results": results}
