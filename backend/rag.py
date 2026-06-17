from langchain_ollama import ChatOllama
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from backend.rag_utils import detect_game, expand_question, is_rules_question
from config import CHROMA_DIR, OLLAMA_BASE_URL, OLLAMA_MODEL

LLM = ChatOllama(model=OLLAMA_MODEL, temperature=0.1, base_url=OLLAMA_BASE_URL)
EMB = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
VS = Chroma(
    collection_name="boardgames",
    embedding_function=EMB,
    persist_directory=str(CHROMA_DIR),
)

PROMPT = ChatPromptTemplate.from_template("""
You are a board game rules expert. Answer using ONLY the context below.

Rules:
- Use only facts present in the context. Do not guess or use outside knowledge.
- If the context does not contain the answer, say clearly that the information was not found in the available documents.
- For rulebook questions, prioritize content from rulebook sources.
- Answer in the same language as the question.
- Be direct and cite the source file name when possible.

Context:
{context}

Question: {question}

Answer:
""")


def format_docs(docs):
    parts = []
    for d in docs:
        source = d.metadata.get("source", "?")
        game = d.metadata.get("game")
        doc_type = d.metadata.get("doc_type", "?")
        header = f"[{source}"
        if game:
            header += f" | {game}"
        header += f" | {doc_type}]"
        parts.append(f"{header}\n{d.page_content}")
    return "\n\n---\n\n".join(parts)


def _unique_docs(docs):
    seen = set()
    unique = []
    for doc in docs:
        key = (doc.metadata.get("source"), doc.page_content[:120])
        if key in seen:
            continue
        seen.add(key)
        unique.append(doc)
    return unique


def retrieve_docs(question: str, k: int = 10):
    game = detect_game(question)
    rules_q = is_rules_question(question)
    search_query = expand_question(question, game)

    docs = VS.similarity_search(search_query, k=k * 3)

    if game:
        game_lower = game.lower()
        game_docs = [
            d
            for d in docs
            if game_lower in str(d.metadata.get("game", "")).lower()
            or game_lower in str(d.metadata.get("source", "")).lower()
        ]
        if game_docs:
            docs = _unique_docs(game_docs + docs)

    if rules_q:
        rulebooks = [d for d in docs if d.metadata.get("doc_type") == "rulebook"]
        others = [d for d in docs if d.metadata.get("doc_type") != "rulebook"]
        docs = _unique_docs(rulebooks + others)

    return docs[:k]


def rag_chain(question: str, k: int = 10):
    docs = retrieve_docs(question, k=k)
    context = format_docs(docs)
    answer = (PROMPT | LLM | StrOutputParser()).invoke(
        {"context": context, "question": question}
    )
    return answer, [d.metadata for d in docs]
