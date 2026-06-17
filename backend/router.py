from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from config import OLLAMA_BASE_URL, OLLAMA_MODEL

LLM = ChatOllama(model=OLLAMA_MODEL, temperature=0, base_url=OLLAMA_BASE_URL)

ROUTE = ChatPromptTemplate.from_template("""
Classify the user's board-game question into ONE label:

- SQL: numeric/aggregate questions about games (ratings, player counts, playtime,
  filtering, ranking, "best", "top", "under X minutes", "by designer", etc.)
- RAG: questions about rules, strategy, themes, reviews, how to play, lore.

Reply with only the label.

Question: {q}
Label:""")


def route(question: str) -> str:
    label = (ROUTE | LLM).invoke({"q": question}).content.strip().upper()
    return "SQL" if "SQL" in label else "RAG"
