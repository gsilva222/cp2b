import json
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DATABASE_URL, GAMES_JSON

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
    if not GAMES_JSON.exists():
        raise FileNotFoundError(f"Missing {GAMES_JSON}")

    engine = create_engine(DATABASE_URL)
    with engine.begin() as c:
        c.execute(text(DDL))
        for g in json.loads(GAMES_JSON.read_text(encoding="utf-8")):
            c.execute(
                text("""
              INSERT INTO games VALUES
              (:bgg_id,:name,:year,:min_players,:max_players,:playtime,:min_age,
               :weight,:rating,:rank,:categories,:mechanics,:designers,:description)
              ON CONFLICT (bgg_id) DO UPDATE SET rating=EXCLUDED.rating
            """),
                g,
            )


if __name__ == "__main__":
    load()
