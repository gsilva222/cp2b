# ingest/load_postgres.py
import json
from sqlalchemy import create_engine, text

DDL = """
CREATE TABLE IF NOT EXISTS games (
  bgg_id INT PRIMARY KEY,
  name TEXT, year INT,
  min_players INT, max_players INT,
  playtime INT, min_age INT,
  weight REAL, rating REAL, rank TEXT,
  categories TEXT[], mechanics TEXT[], designers TEXT[],
  description TEXT
);
"""

def load():
    engine = create_engine(
    "postgresql+psycopg://bg:bg@127.0.0.1:5434/boardgames"
    )
    with engine.begin() as c:
        c.execute(text(DDL))
        for g in json.load(open("data/games.json")):
            c.execute(text("""
              INSERT INTO games VALUES
              (:bgg_id,:name,:year,:min_players,:max_players,:playtime,:min_age,
               :weight,:rating,:rank,:categories,:mechanics,:designers,:description)
              ON CONFLICT (bgg_id) DO UPDATE SET rating=EXCLUDED.rating
            """), g)

if __name__ == "__main__":
    load()