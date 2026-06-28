"""Initial setup: PostgreSQL data + ChromaDB index."""
import os
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ingest.build_vectorstore import build as build_vectorstore
from ingest.index_manifest import current_index_state, index_is_current, save_manifest
from ingest.load_postgres import load as load_postgres


def should_rebuild() -> bool:
    if os.getenv("FORCE_REBUILD", "").lower() in ("1", "true", "yes"):
        return True
    return not index_is_current()


def main() -> None:
    print("Loading PostgreSQL data...")
    load_postgres()
    print("PostgreSQL data loaded.")

    if should_rebuild():
        print("Building vectorstore...")
        build_vectorstore()
        save_manifest(current_index_state())
        print("Vectorstore built and manifest updated.")
    else:
        print("Index is up to date. Skipping vectorstore build.")

    print("Setup complete.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"SETUP FAILED: {exc}")
        traceback.print_exc()
        sys.exit(1)
