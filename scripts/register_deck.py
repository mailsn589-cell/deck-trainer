from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from flashcard_core import register_manifest_entry  # noqa: E402


def register_deck(manifest_path: Path, deck_name: str, file_name: str) -> Path:
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        data = {"decks": []}

    updated = register_manifest_entry(data, deck_name, file_name)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(updated, indent=2, ensure_ascii=True), encoding="utf-8")
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Register or update a deck in decks/manifest.json")
    parser.add_argument("--name", required=True, help="Deck display name")
    parser.add_argument("--file", required=True, help="Deck JSON file name, e.g. notes.json")
    parser.add_argument("--manifest", default="decks/manifest.json", help="Manifest path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    register_deck(manifest_path, args.name, args.file)
    print(f"Updated manifest: {manifest_path}")


if __name__ == "__main__":
    main()

