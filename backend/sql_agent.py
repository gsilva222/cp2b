from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama

from config import DATABASE_URL, OLLAMA_BASE_URL, OLLAMA_MODEL

ENGINE = create_engine(DATABASE_URL)
DB = SQLDatabase(ENGINE, include_tables=["games"])
LLM = ChatOllama(model=OLLAMA_MODEL, temperature=0, base_url=OLLAMA_BASE_URL)

agent = create_sql_agent(llm=LLM, db=DB, verbose=False)


def sql_answer(question: str) -> str:
    return agent.invoke({"input": question})["output"]
