from fastapi import FastAPI
from pydantic import BaseModel

from backend.router import route
from backend.rag import rag_chain
from backend.sql_agent import sql_answer

app = FastAPI(title="BoardGame GPT")


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(q: Query):
    path = route(q.question)
    if path == "SQL":
        return {"path": "SQL", "answer": sql_answer(q.question), "sources": []}
    answer, sources = rag_chain(q.question)
    return {"path": "RAG", "answer": answer, "sources": sources}


@app.get("/health")
def health():
    return {"ok": True}
