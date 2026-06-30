from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from flashcard_core import parse_lines_to_cards  # noqa: E402


def convert_text_to_deck(text: str, output_path: Path, name: str) -> Path:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cards = parse_lines_to_cards(lines)
    deck_data = {"name": name, "cards": cards}

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(deck_data, indent=2, ensure_ascii=True), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert raw text into a flashcard JSON deck.")
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--input-file", help="Path to text file")
    source_group.add_argument("--input-string", help="Raw multiline text")
    parser.add_argument("--output", required=True, help="Output deck JSON path")
    parser.add_argument("--name", required=True, help="Deck name")
    args = parser.parse_args()

    if args.input_file:
        input_text = Path(args.input_file).expanduser().resolve().read_text(encoding="utf-8")
    else:
        input_text = args.input_string

    created = convert_text_to_deck(
        text=input_text,
        output_path=Path(args.output).expanduser().resolve(),
        name=args.name,
    )
    print(f"Created deck: {created}")


if __name__ == "__main__":
    main()

