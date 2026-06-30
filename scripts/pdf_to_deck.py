from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pypdf import PdfReader

# Allow running this script directly from scripts/ while importing project modules.
sys.path.append(str(Path(__file__).resolve().parents[1]))
from flashcard_core import parse_lines_to_cards  # noqa: E402


def read_pdf_lines(pdf_path: Path) -> list[str]:
    text_chunks: list[str] = []
    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        text_chunks.append(page.extract_text() or "")
    joined = "\n".join(text_chunks)
    lines = [line.strip() for line in joined.splitlines()]
    return [line for line in lines if line]


def convert_pdfs_to_deck(input_paths: list[Path], output_path: Path, name: str) -> Path:
    all_lines: list[str] = []
    for path in input_paths:
        all_lines.extend(read_pdf_lines(path))

    deck_data = {"name": name, "cards": parse_lines_to_cards(all_lines)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(deck_data, indent=2, ensure_ascii=True), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert one or more PDFs into a flashcard JSON deck.")
    parser.add_argument("--input", action="append", required=True, help="Input PDF path (repeat --input)")
    parser.add_argument("--output", required=True, help="Output deck JSON path")
    parser.add_argument("--name", required=True, help="Deck name")
    args = parser.parse_args()

    input_paths = [Path(value).expanduser().resolve() for value in args.input]
    output_path = Path(args.output).expanduser().resolve()
    created = convert_pdfs_to_deck(input_paths, output_path, args.name)
    print(f"Created deck: {created}")


if __name__ == "__main__":
    main()
