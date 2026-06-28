import json
import shutil
import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.rag_utils import game_name_from_pdf
from config import CHROMA_DIR, GAMES_JSON, REVIEWS_DIR, RULEBOOKS_DIR


def load_documents():
    docs = []

    if RULEBOOKS_DIR.exists():
        for pdf in RULEBOOKS_DIR.glob("*.pdf"):
            game = game_name_from_pdf(pdf)
            print(f"Loading rulebook: {pdf.name} ({game})")
            try:
                pages = PyPDFLoader(str(pdf)).load()
            except Exception as exc:
                print(f"WARNING: could not read {pdf.name}: {exc}")
                continue
            for d in pages:
                page = d.metadata.get("page", 0)
                if isinstance(page, int):
                    page_label = page + 1
                else:
                    page_label = page
                d.page_content = f"[{game} - pagina {page_label}]\n{d.page_content}"
                d.metadata["source"] = pdf.name
                d.metadata["doc_type"] = "rulebook"
                d.metadata["game"] = game
                docs.append(d)

    if REVIEWS_DIR.exists():
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


def clear_chroma_dir() -> None:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    for item in CHROMA_DIR.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def build():
    docs = load_documents()
    rulebooks = sum(1 for d in docs if d.metadata.get("doc_type") == "rulebook")
    print(f"Loaded {len(docs)} documents ({rulebooks} rulebook pages)")

    if not docs:
        raise RuntimeError("No documents found to index.")

    rulebook_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, chunk_overlap=200
    )
    default_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=120
    )

    chunks = []
    for doc in docs:
        splitter = (
            rulebook_splitter
            if doc.metadata.get("doc_type") == "rulebook"
            else default_splitter
        )
        chunks.extend(splitter.split_documents([doc]))

    clear_chroma_dir()

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    Chroma.from_documents(
        chunks,
        embedding=embeddings,
        collection_name="boardgames",
        persist_directory=str(CHROMA_DIR),
    )
    print(f"Indexed {len(chunks)} chunks from {len(docs)} documents.")
    rulebook_chunks = sum(1 for c in chunks if c.metadata.get("doc_type") == "rulebook")
    print(f"Rulebook chunks: {rulebook_chunks}")


if __name__ == "__main__":
    build()
