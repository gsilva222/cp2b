from langchain_ollama import ChatOllama
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import CHROMA_DIR, OLLAMA_BASE_URL, OLLAMA_MODEL

LLM = ChatOllama(model=OLLAMA_MODEL, temperature=0.2, base_url=OLLAMA_BASE_URL)
EMB = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
VS = Chroma(
    collection_name="boardgames",
    embedding_function=EMB,
    persist_directory=str(CHROMA_DIR),
)

PROMPT = ChatPromptTemplate.from_template("""
You are a knowledgeable board game expert. Answer the user's question using ONLY the
context below. If the answer isn't in the context, say so honestly. Cite sources by name.

Context:
{context}

Question: {question}

Answer:
""")


def format_docs(docs):
    return "\n\n".join(
        f"[{d.metadata.get('source', '?')}] {d.page_content}" for d in docs
    )


def rag_chain(question: str, k: int = 5):
    retriever = VS.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)
    chain = (
        {"context": lambda _: format_docs(docs), "question": RunnablePassthrough()}
        | PROMPT
        | LLM
        | StrOutputParser()
    )
    return chain.invoke(question), [d.metadata for d in docs]
