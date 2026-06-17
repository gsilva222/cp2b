import json
import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import CHROMA_DIR, GAMES_JSON, REVIEWS_DIR, RULEBOOKS_DIR


def load_documents():
    docs = []
    RULEBOOKS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)

    for pdf in RULEBOOKS_DIR.glob("*.pdf"):
        for d in PyPDFLoader(str(pdf)).load():
            d.metadata["source"] = pdf.name
            d.metadata["doc_type"] = "rulebook"
            docs.append(d)

    for txt in REVIEWS_DIR.glob("*.txt"):
        for d in TextLoader(str(txt), encoding="utf-8").load():
            d.metadata["source"] = txt.name
            d.metadata["doc_type"] = "review"
            docs.append(d)

    if GAMES_JSON.exists():
        for g in json.loads(GAMES_JSON.read_text(encoding="utf-8")):
            if g["description"]:
                docs.append(
                    Document(
                        page_content=f"{g['name']} ({g['year']}): {g['description']}",
                        metadata={
                            "source": "bgg",
                            "doc_type": "description",
                            "game": g["name"],
                        },
                    )
                )
    return docs


def build():
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    Chroma.from_documents(
        chunks,
        embedding=embeddings,
        collection_name="boardgames",
        persist_directory=str(CHROMA_DIR),
    )
    print(f"Indexed {len(chunks)} chunks from {len(docs)} documents.")


if __name__ == "__main__":
    build()
