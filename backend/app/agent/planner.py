import json
import re
from langchain_ollama import ChatOllama
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL

def llm():
    return ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.1)

def plan(question: str) -> dict:
    prompt = f'''
You are an agent planner. Choose useful tools for the question.
Tools: document_search (uploaded files), web_search (external/current info), calculator (arithmetic).
Return ONLY JSON: {{"tools":["document_search"],"query":"search terms","calculation":"arithmetic expression","reason":"brief reason"}}
Select one to three tools maximum. Prefer document_search for questions about uploaded material.
Use web_search for current or external information. Use calculator only for arithmetic.
Question: {question}
'''
    raw = str(llm().invoke(prompt).content)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        data = json.loads(match.group(0)) if match else {}
    except Exception:
        data = {}
    allowed = {"document_search", "web_search", "calculator"}
    tools = [t for t in data.get("tools", []) if t in allowed][:3] or ["document_search"]
    return {"tools": tools, "query": str(data.get("query") or question)[:500],
            "calculation": str(data.get("calculation") or "")[:200],
            "reason": str(data.get("reason") or "Default document retrieval")}
