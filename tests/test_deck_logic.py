import unittest

from deck_logic import LearnSession, PracticeSession, build_standard_deck, normalize_card_input


class DeckLogicTests(unittest.TestCase):
    def test_standard_deck_has_52_cards(self):
        deck = build_standard_deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(deck[0], "A of Clubs")
        self.assertEqual(deck[-1], "K of Spades")

    def test_normalize_short_forms(self):
        self.assertEqual(normalize_card_input("QH"), "q of hearts")
        self.assertEqual(normalize_card_input("10s"), "10 of spades")
        self.assertEqual(normalize_card_input("a of clubs"), "a of clubs")

    def test_learn_session_navigation_wraps(self):
        learn = LearnSession(deck=["A", "B", "C"])
        self.assertEqual(learn.current_card(), "A")
        learn.prev_card()
        self.assertEqual(learn.current_card(), "C")
        learn.next_card()
        self.assertEqual(learn.current_card(), "A")

    def test_practice_session_progress_and_guess(self):
        practice = PracticeSession(deck=["A of Clubs", "K of Spades"], seed=1)
        prompt = practice.next_prompt()
        self.assertIsNotNone(prompt)
        self.assertEqual(practice.progress(), (1, 2))

        _, expected = prompt
        correct, _ = practice.check_guess(expected)
        self.assertTrue(correct)


if __name__ == "__main__":
    unittest.main()

