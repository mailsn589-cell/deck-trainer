import importlib
import json
import tempfile
import unittest
from pathlib import Path

from flashcard_core import parse_lines_to_cards, register_manifest_entry, validate_deck_schema
from scripts.pptx_to_deck import convert_pptx_to_deck
from scripts.register_deck import register_deck
from scripts.text_to_deck import convert_text_to_deck


class ConverterTests(unittest.TestCase):
    def test_parse_lines_term_and_bullets(self):
        lines = [
            "GI Symptoms:",
            "Hematemesis: Vomiting blood",
            "Diet",
            "- High fiber",
            "- Adequate hydration",
        ]
        cards = parse_lines_to_cards(lines)
        self.assertGreaterEqual(len(cards), 2)
        for card in cards:
            self.assertTrue(card["front"].strip())
            self.assertTrue(card["back"].strip())

    def test_text_converter_creates_valid_json(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "notes.json"
            convert_text_to_deck("Hematemesis: Vomiting blood\nMelena: Dark stool", out, "Notes")
            deck = json.loads(out.read_text(encoding="utf-8"))
            ok, message = validate_deck_schema(deck)
            self.assertTrue(ok, msg=message)

    def test_pptx_converter_creates_valid_json(self):
        with tempfile.TemporaryDirectory() as td:
            pptx_path = Path(td) / "sample.pptx"
            out = Path(td) / "pptx_deck.json"

            pptx_module = importlib.import_module("pptx")
            prs = pptx_module.Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = "Urinary Symptoms"
            body = slide.placeholders[1].text_frame
            body.text = "Retention"
            body.add_paragraph().text = "Unable to empty bladder"
            prs.save(str(pptx_path))

            convert_pptx_to_deck(pptx_path, out, "PPTX Deck")
            deck = json.loads(out.read_text(encoding="utf-8"))
            ok, message = validate_deck_schema(deck)
            self.assertTrue(ok, msg=message)

    def test_manifest_registration_logic(self):
        base = {"decks": [{"name": "Old", "file": "a.json"}]}
        updated = register_manifest_entry(base, "New", "a.json")
        self.assertEqual(len(updated["decks"]), 1)
        self.assertEqual(updated["decks"][0]["name"], "New")

    def test_register_deck_script_updates_file(self):
        with tempfile.TemporaryDirectory() as td:
            manifest = Path(td) / "manifest.json"
            register_deck(manifest, "Deck One", "deck_one.json")
            register_deck(manifest, "Deck One Updated", "deck_one.json")
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(len(data["decks"]), 1)
            self.assertEqual(data["decks"][0]["name"], "Deck One Updated")


if __name__ == "__main__":
    unittest.main()
