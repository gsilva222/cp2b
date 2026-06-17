# BoardGame GPT

Chatbot sobre jogos de tabuleiro com RAG e SQL Agent. Responde perguntas sobre regras, reviews, ratings e estatísticas com dados do BoardGameGeek (BGG).

---
### Guia

### Passo 1 — Instalar software (só uma vez no PC)

1. **Python 3.12+** → https://www.python.org/downloads/  
   No instalador, marcar **"Add Python to PATH"**.

2. **Docker Desktop** → https://www.docker.com/products/docker-desktop/  
   Instalar, abrir, e aguardar o estado **"Running"** (ícone verde).

Requisitos: Windows 10/11, 8 GB RAM, internet na primeira execução.

### Passo 2 — Setup do projeto (só uma vez)

Copiar ou clonar o projeto para o PC. Abrir **PowerShell** na pasta do projeto:

```powershell
cd C:\caminho\para\cp2b
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

Este comando instala tudo automaticamente:
- Pacotes Python (`venv` + `requirements.txt`)
- Ficheiro `.env`
- Docker (PostgreSQL + Ollama)
- Dados em PostgreSQL
- Índice de embeddings (ChromaDB)
- Modelo `llama3.1:8b`

A primeira vez pode demorar **15–30 minutos** (PyTorch, embeddings, modelo LLM).

### Passo 3 — Usar a aplicação (sempre que quiseres abrir)

Abrir **dois terminais** PowerShell na pasta do projeto:

```powershell
# Terminal 1
cd C:\caminho\para\cp2b
.\scripts\run-backend.ps1
```

```powershell
# Terminal 2
cd C:\caminho\para\cp2b
.\scripts\run-frontend.ps1
```

Abrir no browser: **http://localhost:8501**

> **Importante:** Docker Desktop tem de estar **Running** sempre que usas a app.

---

## O que vem incluído no projeto

Não precisas de descarregar dados manualmente. O repositório já inclui:

- `data/games.json` — 200 jogos com descrições
- `docker-compose.yml` — PostgreSQL + Ollama
- `.env.example` — configuração default

O setup gera automaticamente:
- `venv/` — ambiente Python
- `.env` — cópia de `.env.example`
- `chroma_db/` — vectorstore local

## Exemplos de perguntas

- "Tell me about Stonehenge"
- "What are the best games under 30 minutes?"
- "How to play Piratenbillard?"

## Testar API

```powershell
Invoke-RestMethod -Uri "http://localhost:8080/health"
Invoke-RestMethod -Uri "http://localhost:8080/ask" -Method POST `
  -ContentType "application/json" `
  -Body '{"question": "What games do you have?"}'
```

## Estrutura

```
cp2b/
├── backend/              # FastAPI + LangChain
├── frontend/             # Streamlit
├── ingest/               # Scripts de ingestão
├── scripts/
│   ├── setup.ps1         # Setup completo (correr 1x)
│   ├── run-backend.ps1   # API na porta 8080
│   └── run-frontend.ps1  # UI na porta 8501
├── data/games.json       # Dados incluídos
├── config.py
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

## Configuração (.env)

Criado automaticamente pelo setup. Só editar se precisares:

| Variável | Default | Descrição |
|----------|---------|-----------|
| `DATABASE_URL` | `postgresql+psycopg://bg:bg@127.0.0.1:5434/boardgames` | PostgreSQL |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | API Ollama |
| `OLLAMA_MODEL` | `llama3.1:8b` | Modelo LLM |
| `API_URL` | `http://localhost:8080/ask` | URL do backend |

Trocar modelo:
```powershell
docker exec (docker compose ps -q ollama) ollama pull llama3.2
```
Editar `.env`: `OLLAMA_MODEL=llama3.2`

## Dados extra (opcional)

- PDFs → `data/rulebooks/`
- Reviews `.txt` → `data/reviews/`
- Depois: `.\venv\Scripts\python.exe ingest\build_vectorstore.py`

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `ExecutionPolicy` | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `Python not found` | Reinstalar Python com "Add Python to PATH" |
| `Docker Desktop is not running` | Abrir Docker Desktop e aguardar "Running" |
| `Virtual environment not found` | Correr `.\scripts\setup.ps1` |
| `pip install failed` | `.\venv\Scripts\python.exe -m pip install -r requirements.txt` |
| `model not found` | `docker exec (docker compose ps -q ollama) ollama pull llama3.1:8b` |
| Erro JSON no frontend | Iniciar `run-backend.ps1` antes do frontend |
| PostgreSQL not ready | `docker compose ps` — aguardar container "Up" e repetir setup |

## Tecnologias

FastAPI · Streamlit · LangChain · Ollama · PostgreSQL · ChromaDB · Sentence Transformers

## Licença

Projeto educacional. Dados do BGG — respeita copyrights.
