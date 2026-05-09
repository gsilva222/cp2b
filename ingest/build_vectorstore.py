# ingest/build_vectorstore.py
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma

def load_documents():
    docs = []
    for pdf in Path("data/rulebooks").glob("*.pdf"):
        for d in PyPDFLoader(str(pdf)).load():
            d.metadata["source"] = pdf.name
            d.metadata["doc_type"] = "rulebook"
            docs.append(d)
    for txt in Path("data/reviews").glob("*.txt"):
        for d in TextLoader(str(txt)).load():
            d.metadata["source"] = txt.name
            d.metadata["doc_type"] = "review"
            docs.append(d)
    # also add BGG descriptions as docs
    import json
    for g in json.load(open("data/games.json")):
        if g["description"]:
            from langchain_core.documents import Document
            docs.append(Document(
                page_content=f"{g['name']} ({g['year']}): {g['description']}",
                metadata={"source": "bgg", "doc_type": "description", "game": g["name"]}
            ))
    return docs

def build():
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    Chroma.from_documents(
        chunks,
        embedding=embeddings,
        collection_name="boardgames",
        persist_directory="./chroma_db",
    )
    print(f"Indexed {len(chunks)} chunks from {len(docs)} documents.")

if __name__ == "__main__":
    build()