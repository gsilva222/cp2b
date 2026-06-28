# BoardGame GPT

Chatbot sobre jogos de tabuleiro com RAG e SQL Agent. Responde perguntas sobre regras, reviews, ratings e estatísticas com dados do BoardGameGeek (BGG).

O projeto corre em **Docker**. Não é necessário instalar Python no PC.

> **Nota:** O Docker Desktop **não executa** o `docker-compose.yml` apenas pela interface gráfica. É preciso arrancar o projeto **uma vez pela linha de comandos**. Depois disso, podes **iniciar e parar** os contentores pelo Docker Desktop.

---

## Requisitos

* Windows 10/11
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* 8 GB RAM (recomendado 16 GB)
* Internet na primeira execução

---

## Como arrancar

### 1. Instalar e abrir o Docker Desktop

Instalar o Docker Desktop e abrir a aplicação. Aguardar até o estado ficar **Running** (ícone verde).

### 2. Primeira execução (linha de comandos)

Abrir **PowerShell** ou **Terminal** na pasta do projeto e executar:

```powershell
cd C:\caminho\para\cp2b
docker compose up -d --build
```

Este comando (só na primeira vez, ou quando alteras o código):

* Constrói a imagem da aplicação
* Arranca PostgreSQL e Ollama
* Executa o contentor **setup** (carrega dados, indexa textos, descarrega modelo)
* Arranca **backend** e **frontend**

A primeira execução pode demorar **15 a 30 minutos**.

Verificar no Docker Desktop se os contentores estão a correr:

| Contentor | Estado esperado |
|-----------|-----------------|
| `postgres` | Running |
| `ollama` | Running |
| `setup` | Exited (0) |
| `backend` | Running |
| `frontend` | Running |

### 3. Abrir a aplicação

No browser: **http://localhost:8501**

### 4. Arranques seguintes (Docker Desktop)

Depois da primeira execução, o projeto fica registado no Docker Desktop. Podes gerir sem linha de comandos:

1. Abrir o **Docker Desktop**
2. Ir a **Containers** (ou ao projeto **boardgame-gpt**)
3. Clicar em **Start** (▶) para arrancar todos os contentores
4. Clicar em **Stop** (■) para parar

> Se os contentores não aparecerem, repetir o passo 2 (`docker compose up -d`).

---

## Parar o projeto

**Pelo Docker Desktop:** selecionar o projeto e clicar **Stop**.

**Pela linha de comandos:**

```powershell
docker compose down
```

---

## Adicionar rulebooks (ex.: Catan)

### 1. Colocar o PDF na pasta

```
data/rulebooks/catan-rules.pdf
```

Convém usar nomes como `nome-do-jogo-rules.pdf`.

### 2. Reindexar (obrigatório)

O contentor **setup** só indexa PDFs novos quando volta a correr. Tens duas opções:

**Opção A — Linha de comandos (recomendada)**

```powershell
cd C:\projetos\git\cp2b
docker compose run --rm setup
docker compose restart backend
```

**Opção B — Docker Desktop**

1. Parar o contentor **backend** (Stop)
2. Clicar **Play** no contentor **setup** (volta a correr e deteta PDFs novos)
3. Verificar nos **Logs** do setup: `Building vectorstore...` e `Rulebook chunks: ...`
4. Arrancar o **backend** de novo (Play)

> **Nota:** `setup` e `ollama-init` ficam **Exited** quando terminam. Isso é normal. Os que têm de estar **Running** para usar a app são: `postgres`, `ollama`, `backend` e `frontend`.

### 3. Testar

Perguntar algo sobre o jogo, por exemplo: *"Qual é o objetivo do Catan?"*

Deves ver **Rota: RAG** e **Fontes:** com `catan-rules.pdf`.

---

## Contentores em execução

| Contentor | Estado normal | Função |
|-----------|---------------|--------|
| `postgres` | Running | Base de dados |
| `ollama` | Running | Modelo de IA |
| `ollama-init` | Exited (0) | Descarrega modelo (1x) |
| `setup` | Exited (0) | Indexa dados (corre quando necessário) |
| `backend` | Running | API |
| `frontend` | Running | Interface web |

---

## Estrutura do projeto

```
cp2b/
├── backend/           # API FastAPI + RAG + SQL Agent
├── frontend/          # Interface Streamlit
├── ingest/            # Scripts de ingestão
├── data/              # Jogos, rulebooks, reviews
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Contentores Docker

| Serviço | Função | Porta |
|---------|--------|-------|
| `postgres` | Base de dados dos jogos | interna |
| `ollama` | Modelo de IA local | interna |
| `ollama-init` | Descarrega o modelo Ollama | — |
| `setup` | Carrega dados e cria índice | — |
| `backend` | API da aplicação | 8080 |
| `frontend` | Interface web | 8501 |

## Tecnologias

FastAPI · Streamlit · LangChain · Ollama · PostgreSQL · ChromaDB · Sentence Transformers · Docker Compose

## Resolução de problemas

### Ver logs de um contentor que falhou

No PowerShell, na pasta do projeto:

```powershell
docker logs boardgame-gpt-setup-1
docker logs boardgame-gpt-ollama-init-1
```

No **Docker Desktop**: clicar no contentor → separador **Logs**.

| Problema | Solução |
|----------|---------|
| `setup` falhou (exit 1) | Ver logs: `docker logs boardgame-gpt-setup-1` |
| `ollama-init` falhou | Ver logs: `docker logs boardgame-gpt-ollama-init-1` — pode ser falta de RAM |
| Projeto não aparece no Docker Desktop | Executar `docker compose up -d --build` na pasta do projeto |
| Docker não arranca | Abrir Docker Desktop e aguardar "Running" |
| Frontend sem resposta | Verificar se **backend** está Running |
| "model not found" | Ver logs do **ollama-init** |
| Primeira execução lenta | Normal |
| Regras do PDF não aparecem | Correr `docker compose run --rm setup` e `docker compose restart backend` |
| Fontes não aparecem | Só aparecem em perguntas **RAG** (regras, objetivos). Perguntas SQL não têm fontes |

## Licença

Projeto educacional. Dados do BGG — respeita copyrights.
