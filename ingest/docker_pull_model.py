"""Download Ollama model (runs in separate container)."""
import json
import sys
import time
import traceback
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import OLLAMA_BASE_URL, OLLAMA_MODEL


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
    return any(
        name == OLLAMA_MODEL or name.startswith(f"{OLLAMA_MODEL}")
        for name in names
    )


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
            if status.get("error"):
                raise RuntimeError(status["error"])


def main() -> None:
    wait_for_ollama()
    pull_ollama_model()
    print("Ollama model ready.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"OLLAMA INIT FAILED: {exc}")
        traceback.print_exc()
        sys.exit(1)
