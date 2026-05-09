import json, csv
from pathlib import Path

def fetch_top_games(n=200):
    csv_path = Path("data/games.csv")
    if not csv_path.exists():
        raise FileNotFoundError(
            "Ficheiro data/games.csv não encontrado.\n"
            "Faz download em: https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek\n"
            "e coloca-o na pasta data/"
        )

    print(f"A ler {csv_path}...")
    games = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print(f"Colunas encontradas: {reader.fieldnames}")

        for i, row in enumerate(reader):
            if len(games) >= n:
                break
            try:
                # Tenta rating - filtra jogos sem avaliação
                rating = float(row.get("AvgRating") or row.get("avg_rating") or 0)
                if rating < 5.0:
                    continue

                games.append({
                    "bgg_id": int(row.get("BGGId") or row.get("bgg_id") or i),
                    "name": row.get("Name") or row.get("name") or "Unknown",
                    "year": int(row.get("YearPublished") or row.get("year_published") or 0),
                    "min_players": int(row.get("MinPlayers") or row.get("min_players") or 1),
                    "max_players": int(row.get("MaxPlayers") or row.get("max_players") or 4),
                    "playtime": int(row.get("MfgPlaytime") or row.get("playtime") or 60),
                    "min_age": int(row.get("MfgAgeRec") or row.get("min_age") or 10),
                    "weight": float(row.get("ComAgeRec") or row.get("weight") or 2.0),
                    "rating": rating,
                    "rank": str(row.get("Rank:boardgame") or row.get("rank") or i+1),
                    "categories": [c.strip() for c in (row.get("GameType") or "").split(",") if c.strip()],
                    "mechanics": [m.strip() for m in (row.get("Mechanics") or "").split(",") if m.strip()],
                    "designers": [row.get("Designer") or "Unknown"],
                    "description": (row.get("Description") or "")[:2000],
                })
            except Exception as e:
                print(f"Linha {i} ignorada: {e}")

    Path("data/games.json").write_text(json.dumps(games, indent=2), encoding="utf-8")
    print(f"Guardados {len(games)} jogos em data/games.json")
    return games


if __name__ == "__main__":
    fetch_top_games(200)