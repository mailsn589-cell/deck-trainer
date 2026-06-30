from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader


def read_pdf_lines(pdf_path: Path) -> list[str]:
    text_chunks: list[str] = []
    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        text_chunks.append(page.extract_text() or "")
    joined = "\n".join(text_chunks)
    lines = [line.strip() for line in joined.splitlines()]
    return [line for line in lines if line]


def normalize_line(line: str) -> str:
    cleaned = line.replace("\u2022", "-").replace("\u25aa", "-")
    return re.sub(r"\s+", " ", cleaned).strip()


def looks_like_heading(line: str) -> bool:
    if len(line) > 60:
        return False
    if line.endswith(":"):
        return True
    words = line.split()
    return 1 <= len(words) <= 6 and all(w[:1].isupper() for w in words if w[:1].isalpha())


def parse_cards(lines: Iterable[str]) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    current_topic = "General"
    current_term = ""
    current_points: list[str] = []

    def flush_current() -> None:
        nonlocal current_term, current_points
        if current_term and current_points:
            cards.append({"front": current_term, "back": " ".join(current_points), "topic": current_topic})
        current_term = ""
        current_points = []

    for raw_line in lines:
        line = normalize_line(raw_line)
        if not line or re.fullmatch(r"\d+", line):
            continue

        if looks_like_heading(line):
            flush_current()
            current_topic = line.rstrip(":")
            continue

        qa_match = re.match(r"^([^:]{2,60}):\s+(.+)$", line)
        if qa_match:
            flush_current()
            current_term = qa_match.group(1).strip()
            current_points = [qa_match.group(2).strip()]
            continue

        if line.startswith("-"):
            bullet_text = line.lstrip("- ").strip()
            if current_term:
                current_points.append(bullet_text)
            else:
                cards.append({"front": f"{current_topic} note {len(cards) + 1}", "back": bullet_text, "topic": current_topic})
            continue

        if current_term:
            current_points.append(line)
        else:
            current_term = line

    flush_current()

    if not cards:
        compact = [normalize_line(v) for v in lines if normalize_line(v)]
        for idx in range(0, len(compact), 2):
            front = compact[idx]
            back = compact[idx + 1] if idx + 1 < len(compact) else "Review this concept"
            cards.append({"front": front, "back": back, "topic": "General"})

    return cards


def convert_pdfs_to_deck(input_paths: list[Path], output_path: Path, name: str) -> Path:
    all_lines: list[str] = []
    for path in input_paths:
        all_lines.extend(read_pdf_lines(path))

    deck_data = {"name": name, "cards": parse_cards(all_lines)}
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

