# backend/sql_agent.py
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama
from langchain_community.embeddings import SentenceTransformerEmbeddings

ENGINE = create_engine("postgresql+psycopg2://bg:bg@localhost:5434/boardgames")
DB = SQLDatabase(ENGINE, include_tables=["games"])
LLM = ChatOllama(model="llama3:instruct", temperature=0)

agent = create_sql_agent(llm=LLM, db=DB, verbose=False)

def sql_answer(question: str) -> str:
    return agent.invoke({"input": question})["output"]