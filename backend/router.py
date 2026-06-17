from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from backend.rag_utils import detect_game, is_rules_question
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

LLM = ChatOllama(model=OLLAMA_MODEL, temperature=0, base_url=OLLAMA_BASE_URL)

ROUTE = ChatPromptTemplate.from_template("""
Classify the user's board-game question into ONE label:

- SQL: numeric/aggregate questions about games (ratings, player counts, playtime,
  filtering, ranking, "best", "top", "under X minutes", "by designer", etc.)
  ONLY when asking about statistics across many games or database-style queries.
- RAG: questions about rules, strategy, themes, reviews, how to play, objectives,
  setup, lore, or questions about a specific game's rules even if they mention
  player counts or playtime.

Reply with only the label.

Question: {q}
Label:""")


def route(question: str) -> str:
    if is_rules_question(question) or detect_game(question):
        return "RAG"

    label = (ROUTE | LLM).invoke({"q": question}).content.strip().upper()
    return "SQL" if "SQL" in label else "RAG"
