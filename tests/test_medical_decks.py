import json
import unittest
from pathlib import Path

from flashcard_core import validate_deck_schema
from medical_decks import MEDICAL_DECKS


class MedicalDeckTests(unittest.TestCase):
    def test_expected_decks_exist(self):
        self.assertIn("Abdomen and GI", MEDICAL_DECKS)
        self.assertIn("Rectum and Genitourinary", MEDICAL_DECKS)

    def test_cards_have_front_and_back(self):
        for deck_name, cards in MEDICAL_DECKS.items():
            self.assertGreaterEqual(len(cards), 20, msg=f"Deck too small: {deck_name}")
            for card in cards:
                self.assertIn("front", card)
                self.assertIn("back", card)
                self.assertTrue(card["front"].strip())
                self.assertTrue(card["back"].strip())

    def test_json_decks_match_schema(self):
        root = Path(__file__).resolve().parents[1]
        manifest_path = root / "decks" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertIn("decks", manifest)
        self.assertGreater(len(manifest["decks"]), 0)

        for deck_ref in manifest["decks"]:
            deck_path = root / "decks" / deck_ref["file"]
            self.assertTrue(deck_path.exists(), msg=f"Missing deck file: {deck_ref['file']}")
            deck_data = json.loads(deck_path.read_text(encoding="utf-8"))
            ok, message = validate_deck_schema(deck_data)
            self.assertTrue(ok, msg=message)


if __name__ == "__main__":
    unittest.main()
