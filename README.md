# BoardGame GPT

Chatbot sobre jogos de tabuleiro com RAG e SQL Agent. Responde perguntas sobre regras, reviews, ratings e estatísticas com dados do BoardGameGeek (BGG).

O projeto corre **inteiramente em Docker**. Não é necessário Python instalado nem linha de comandos.

---

## Requisitos

* Windows 10/11
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* 8 GB RAM (recomendado 16 GB)
* Internet na primeira execução

---

## Como arrancar (só Docker Desktop)

### 1. Instalar Docker Desktop

Instalar e abrir o **Docker Desktop**. Aguardar até o estado ficar **Running** (ícone verde).

### 2. Importar o projeto no Docker Desktop

**Opção A (recomendada)**

1. Abrir o **Docker Desktop**
2. No menu lateral, clicar em **Compose** (ou **Containers**)
3. Clicar em **Open** / **Import** / **Create**
4. Selecionar a **pasta do projeto** (a pasta que contém o ficheiro `docker-compose.yml`)
5. O Docker Desktop deteta o projeto **boardgame-gpt**

**Opção B**

1. No Explorador de Ficheiros, ir à pasta do projeto
2. Clicar com o botão direito no ficheiro `docker-compose.yml`
3. Escolher **Open with Docker Desktop** (se disponível)

### 3. Arrancar o projeto

1. No Docker Desktop, com o projeto **boardgame-gpt** visível
2. Clicar no botão **Run** / **Play** (▶)
3. O Docker Desktop vai:
   * Construir a imagem da aplicação (primeira vez)
   * Arrancar PostgreSQL e Ollama
   * Executar o contentor **setup** (carrega dados e indexa textos)
   * Arrancar **backend** e **frontend**

### 4. Aguardar os contentores

Na lista de contentores, verificar o estado:

| Contentor | Estado esperado |
|-----------|-----------------|
| `postgres` | Running (verde) |
| `ollama` | Running (verde) |
| `setup` | Exited (0) — corre uma vez e termina |
| `backend` | Running (verde) |
| `frontend` | Running (verde) |

A **primeira execução** pode demorar 15 a 30 minutos (construção da imagem, download do modelo Ollama e indexação).

### 5. Abrir a aplicação

No browser: **http://localhost:8501**

---

## Parar o projeto

No Docker Desktop, selecionar o projeto **boardgame-gpt** e clicar em **Stop** (■).

---

## Adicionar rulebooks (ex.: Catan)

1. Colocar o PDF em `data/rulebooks/` (ex.: `catan-rules.pdf`)
2. No Docker Desktop, ir a **Volumes**
3. Apagar o volume **boardgame-gpt_chroma_data**
4. Parar e voltar a arrancar o projeto (▶)

O contentor **setup** volta a indexar os ficheiros.

---

## Estrutura do projeto

```
cp2b/
├── backend/           # API FastAPI + RAG + SQL Agent
├── frontend/          # Interface Streamlit
├── ingest/            # Scripts de ingestão
├── data/              # Jogos, rulebooks, reviews
├── Dockerfile         # Imagem da aplicação
├── docker-compose.yml # Configuração dos contentores
└── requirements.txt
```

## Contentores Docker

| Serviço | Função | Porta |
|---------|--------|-------|
| `postgres` | Base de dados dos jogos | interna |
| `ollama` | Modelo de IA local | interna |
| `setup` | Carrega dados e cria índice (1x por arranque) | — |
| `backend` | API da aplicação | 8080 |
| `frontend` | Interface web | 8501 |

## Tecnologias

FastAPI · Streamlit · LangChain · Ollama · PostgreSQL · ChromaDB · Sentence Transformers · Docker Compose

## Resolução de problemas

| Problema | Solução |
|----------|---------|
| Docker não arranca | Abrir Docker Desktop e aguardar "Running" |
| `setup` falhou | Ver logs do contentor **setup** no Docker Desktop |
| Frontend sem resposta | Verificar se **backend** está Running |
| "model not found" | Ver logs do **setup** — o modelo é descarregado no primeiro arranque |
| Primeira execução lenta | Normal — construção da imagem e download do modelo |
| Regras do PDF não aparecem | Apagar volume `chroma_data` e reiniciar o projeto |

## Licença

Projeto educacional. Dados do BGG — respeita copyrights.
