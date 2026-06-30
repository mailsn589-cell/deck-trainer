from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from flashcard_core import parse_lines_to_cards  # noqa: E402


def read_pptx_lines(pptx_path: Path) -> list[str]:
    pptx_module = importlib.import_module("pptx")
    prs = pptx_module.Presentation(str(pptx_path))
    lines: list[str] = []

    for slide in prs.slides:
        title_text = ""
        if slide.shapes.title is not None and slide.shapes.title.text:
            title_text = slide.shapes.title.text.strip()

        if title_text:
            lines.append(f"{title_text}:")

        for shape in slide.shapes:
            if not hasattr(shape, "text_frame") or shape.text_frame is None:
                continue
            for paragraph in shape.text_frame.paragraphs:
                text = paragraph.text.strip()
                if not text or text == title_text:
                    continue
                if paragraph.level > 0:
                    lines.append(f"- {text}")
                else:
                    lines.append(text)

    return lines


def convert_pptx_to_deck(input_path: Path, output_path: Path, name: str) -> Path:
    lines = read_pptx_lines(input_path)
    cards = parse_lines_to_cards(lines)
    deck_data = {"name": name, "cards": cards}

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(deck_data, indent=2, ensure_ascii=True), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a PPTX file into a flashcard JSON deck.")
    parser.add_argument("--input", required=True, help="Input PPTX file")
    parser.add_argument("--output", required=True, help="Output deck JSON path")
    parser.add_argument("--name", required=True, help="Deck name")
    args = parser.parse_args()

    created = convert_pptx_to_deck(
        input_path=Path(args.input).expanduser().resolve(),
        output_path=Path(args.output).expanduser().resolve(),
        name=args.name,
    )
    print(f"Created deck: {created}")


if __name__ == "__main__":
    main()
