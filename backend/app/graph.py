from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.agent.planner import llm, plan
from app.tools.document_search import document_search
from app.tools.web_search import web_search
from app.tools.calculator import calculate

class State(TypedDict, total=False):
    question: str
    plan: dict
    outputs: list[dict]
    activity: list[str]
    answer: str
    sources: list[dict]

def planner_node(state: State):
    p = plan(state["question"])
    return {"plan": p, "outputs": [],
            "activity": [f"Plan: {p['reason']}", f"Selected tools: {', '.join(p['tools'])}"]}

def tools_node(state: State):
    p, outputs = state["plan"], []
    activity = list(state.get("activity", []))
    for name in p["tools"]:
        activity.append(f"Executing {name}")
        if name == "document_search":
            outputs.append(document_search(p["query"]))
        elif name == "web_search":
            outputs.append(web_search(p["query"]))
        elif name == "calculator":
            outputs.append(calculate(p["calculation"]))
    return {"outputs": outputs, "activity": activity}

def answer_node(state: State):
    prompt = (
        "Answer the user's question using the tool evidence. Do not invent facts or citations. "
        "Say clearly if evidence is insufficient. Distinguish document evidence from web results.\n"
        f"Question: {state['question']}\nTool evidence: {state.get('outputs', [])}"
    )
    answer = str(llm().invoke(prompt).content)
    sources = []
    for out in state.get("outputs", []):
        for item in out.get("results", []):
            if item.get("source"):
                sources.append({"name": item["source"], "type": "document"})
            elif item.get("href"):
                sources.append({"name": item.get("title") or item["href"],
                                "type": "web", "url": item["href"]})
    return {"answer": answer, "sources": sources,
            "activity": state.get("activity", []) + ["Synthesizing tool results"]}

builder = StateGraph(State)
builder.add_node("planner", planner_node)
builder.add_node("tools", tools_node)
builder.add_node("answer", answer_node)
builder.add_edge(START, "planner")
builder.add_edge("planner", "tools")
builder.add_edge("tools", "answer")
builder.add_edge("answer", END)
agent = builder.compile()

def run_agent(question: str) -> dict:
    result = agent.invoke({"question": question})
    return {"answer": result["answer"], "tools_used": result["plan"]["tools"],
            "activity": result["activity"], "sources": result["sources"]}
