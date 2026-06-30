import unittest

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


if __name__ == "__main__":
    unittest.main()

