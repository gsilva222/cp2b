# 🎲 BoardGame GPT

Um chatbot inteligente sobre jogos de tabuleiro, usando RAG (Retrieval-Augmented Generation) e SQL Agent para responder perguntas sobre regras, reviews, ratings e mais. Baseado em dados do BoardGameGeek (BGG).

## 📋 Descrição

Este projeto combina:
- **RAG**: Para perguntas sobre regras, estratégias, temas e reviews (usando embeddings e ChromaDB).
- **SQL Agent**: Para perguntas numéricas/estatísticas sobre jogos (ratings, player counts, etc., usando PostgreSQL).
- **Frontend**: Interface Streamlit simples para interagir.
- **Backend**: FastAPI com LangChain e Ollama para IA.

Dados incluem jogos, reviews e rulebooks indexados localmente.

## 🛠️ Pré-requisitos

- **Ubuntu/Linux** (ou similar com Docker).
- **Docker** e **Docker Compose** instalados.
- **Python 3.12+**.
- Pelo menos 8GB RAM (para modelos Ollama).
- Conexão à internet para baixar modelos.

## 🚀 Instalação e Configuração

### 1. Instalar Docker (se não tiver)
```bash
# Adicionar chave GPG
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Adicionar repositório
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# Adicionar usuário ao grupo Docker
sudo usermod -aG docker $USER
# Logout e login novamente, ou execute: newgrp docker
```

### 2. Clonar ou navegar para o projeto
```bash
cd ~/Documents/AOP/CP2B  # Ajusta o caminho se necessário
```

### 3. Criar ambiente virtual Python
```bash
python3 -m venv venv
source venv/bin/activate  # Ativar sempre antes de usar Python
```

### 4. Instalar dependências
```bash
python -m pip install -r requirements.txt
```

### 5. Iniciar serviços Docker (PostgreSQL, Ollama, ChromaDB)
```bash
docker-compose up -d
```
Aguarda 30-60 segundos para os containers iniciarem.

### 6. Popular a base de dados
```bash
# PostgreSQL com dados dos jogos
python ingest/load_postgres.py

# Vectorstore (ChromaDB) com embeddings de reviews/rulebooks
python ingest/build_vectorstore.py
```

### 7. Baixar modelo Ollama
```bash
# Verificar modelos disponíveis
sudo docker exec -it cp2b-ollama-1 ollama list

# Baixar modelo (ex.: llama3.1:8b ou llama3.2)
sudo docker exec -it cp2b-ollama-1 ollama pull llama3.1:8b  # Ajusta se necessário
```
Se o modelo 'llama3.1:8b' não existir, usa `llama3.2` ou `llama3:instruct` e edita `backend/router.py` e `backend/rag.py` para mudar `model="llama3.1:8b"` para o nome correto.

## 🎮 Como Usar

### Iniciar o Backend
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080
```

### Iniciar o Frontend (em outro terminal)
```bash
streamlit run frontend/app.py
```

Abre `http://localhost:8501` no browser. Faz perguntas como:
- "Tell me about Stonehenge"
- "What are the best games under 30 minutes?"
- "How to play Piratenbillard?"

### Testar API diretamente
```bash
curl -X POST "http://localhost:8080/ask" -H "Content-Type: application/json" -d '{"question": "What games do you have?"}'
```

## 📁 Estrutura do Projeto

```
CP2B/
├── backend/              # API FastAPI
│   ├── main.py          # Endpoint principal
│   ├── router.py        # Classificação de perguntas (SQL vs RAG)
│   ├── rag.py           # Cadeia RAG com Ollama
│   └── sql_agent.py     # Agent SQL com PostgreSQL
├── frontend/            # Interface Streamlit
│   └── app.py
├── ingest/              # Scripts de ingestão de dados
│   ├── load_postgres.py # Carrega dados para PostgreSQL
│   ├── build_vectorstore.py # Cria embeddings e indexa em ChromaDB
│   └── fetch_bgg.py     # (Opcional) Busca dados do BGG
├── data/                # Dados brutos
│   ├── games.csv/json   # Lista de jogos
│   ├── reviews/         # Reviews de jogos
│   └── rulebooks/       # Rulebooks
├── chroma_db/           # Vectorstore persistido
├── docker-compose.yml   # Serviços Docker
├── requirements.txt     # Dependências Python
└── README.md            # Este ficheiro
```

## 🧠 Tecnologias

- **Backend**: FastAPI, LangChain, Ollama
- **Frontend**: Streamlit
- **BD**: PostgreSQL (dados estruturados), ChromaDB (vetores)
- **IA**: Llama 3.x via Ollama (local, sem APIs externas)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Infra**: Docker Compose

## 🔧 Troubleshooting

- **Erro "model not found"**: Baixa o modelo correto no Ollama (passo 7).
- **Erro SQLAlchemy**: Certifica-te de que o Docker está a correr e a BD populada.
- **Erro JSON no frontend**: Backend não está a correr – verifica logs.
- **Sem dados**: Re-executa `ingest/load_postgres.py` e `ingest/build_vectorstore.py`.
- **Permissões Docker**: Usa `sudo` ou adiciona usuário ao grupo Docker.

## 📄 Licença

Este projeto é para fins educacionais. Dados do BGG – respeita copyrights.

---

**Nota**: Primeiro run pode demorar devido a downloads de modelos/embeddings. Se tiveres problemas, verifica os logs do backend/frontend.