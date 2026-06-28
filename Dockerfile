FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download embedding model (avoids failure during setup)
RUN python -c "from langchain_community.embeddings import SentenceTransformerEmbeddings; SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')"

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql+psycopg://bg:bg@postgres:5432/boardgames
ENV OLLAMA_BASE_URL=http://ollama:11434
ENV OLLAMA_MODEL=llama3.1:8b
ENV CHROMA_DIR=/app/chroma_db
ENV API_URL=http://backend:8080/ask
