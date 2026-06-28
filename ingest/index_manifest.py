"""Track indexed files so setup rebuilds when rulebooks change."""
import json
from pathlib import Path

from config import CHROMA_DIR, GAMES_JSON, REVIEWS_DIR, RULEBOOKS_DIR

MANIFEST = CHROMA_DIR / ".index_manifest.json"


def _file_state(path: Path) -> dict:
    stat = path.stat()
    return {"path": str(path.name), "size": stat.st_size, "mtime": stat.st_mtime}


def current_index_state() -> dict:
    state = {"rulebooks": [], "reviews": [], "games_json": None}
    if RULEBOOKS_DIR.exists():
        state["rulebooks"] = sorted(
            [_file_state(p) for p in RULEBOOKS_DIR.glob("*.pdf")],
            key=lambda x: x["path"],
        )
    if REVIEWS_DIR.exists():
        state["reviews"] = sorted(
            [_file_state(p) for p in REVIEWS_DIR.glob("*.txt")],
            key=lambda x: x["path"],
        )
    if GAMES_JSON.exists():
        state["games_json"] = _file_state(GAMES_JSON)
    return state


def load_manifest() -> dict | None:
    if not MANIFEST.exists():
        return None
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_manifest(state: dict) -> None:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(state, indent=2), encoding="utf-8")


def index_is_current() -> bool:
    if not CHROMA_DIR.exists() or not any(CHROMA_DIR.iterdir()):
        return False
    saved = load_manifest()
    if saved is None:
        return False
    return saved == current_index_state()
