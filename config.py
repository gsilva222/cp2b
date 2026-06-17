"""Paths and settings for the project."""
from pathlib import Path
import os

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
GAMES_JSON = DATA_DIR / "games.json"
RULEBOOKS_DIR = DATA_DIR / "rulebooks"
REVIEWS_DIR = DATA_DIR / "reviews"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://bg:bg@127.0.0.1:5434/boardgames",
)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
API_URL = os.getenv("API_URL", "http://localhost:8080/ask")
