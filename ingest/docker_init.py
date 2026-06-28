"""Initial setup run inside Docker before backend starts."""
import json
import os
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import CHROMA_DIR, OLLAMA_BASE_URL, OLLAMA_MODEL
from ingest.build_vectorstore import build as build_vectorstore
from ingest.load_postgres import load as load_postgres


def wait_for_ollama(max_attempts: int = 60) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
            if response.ok:
                print("Ollama is ready.")
                return
        except requests.RequestException:
            pass
        print(f"Waiting for Ollama ({attempt}/{max_attempts})...")
        time.sleep(3)
    raise RuntimeError("Ollama did not start in time.")


def ollama_has_model() -> bool:
    response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
    response.raise_for_status()
    names = [model["name"] for model in response.json().get("models", [])]
    return any(name == OLLAMA_MODEL or name.startswith(f"{OLLAMA_MODEL}") for name in names)


def pull_ollama_model() -> None:
    if ollama_has_model():
        print(f"Model {OLLAMA_MODEL} already available.")
        return

    print(f"Pulling model {OLLAMA_MODEL} (this may take several minutes)...")
    with requests.post(
        f"{OLLAMA_BASE_URL}/api/pull",
        json={"name": OLLAMA_MODEL},
        stream=True,
        timeout=3600,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            status = json.loads(line)
            if "status" in status:
                print(status["status"])


def chroma_ready() -> bool:
    return CHROMA_DIR.exists() and any(CHROMA_DIR.iterdir())


def main() -> None:
    wait_for_ollama()
    pull_ollama_model()

    print("Loading PostgreSQL data...")
    load_postgres()

    if chroma_ready() and os.getenv("FORCE_REBUILD", "").lower() not in ("1", "true", "yes"):
        print("ChromaDB already indexed. Skipping vectorstore build.")
    else:
        print("Building vectorstore...")
        build_vectorstore()

    print("Setup complete.")


if __name__ == "__main__":
    main()
