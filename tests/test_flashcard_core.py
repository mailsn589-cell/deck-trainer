import unittest

from flashcard_core import (
    default_progress,
    filter_card_indices,
    schedule_next,
    sort_due_first,
    validate_deck_schema,
)


class FlashcardCoreTests(unittest.TestCase):
    def test_schedule_again_resets_streak(self):
        state = default_progress()
        state["streak"] = 3
        next_state = schedule_next(state, "again", now_ts=1000.0)
        self.assertEqual(next_state["streak"], 0)
        self.assertGreater(next_state["due_timestamp"], 1000.0)

    def test_schedule_easy_increases_interval(self):
        state = default_progress()
        state["interval_days"] = 2.0
        next_state = schedule_next(state, "easy", now_ts=1000.0)
        self.assertGreater(next_state["interval_days"], 2.0)
        self.assertGreater(next_state["ease"], 2.5)

    def test_filter_indices_by_query_and_topic(self):
        cards = [
            {"front": "Hematemesis", "back": "Vomiting blood", "topic": "Symptoms"},
            {"front": "Melena", "back": "Tarry stool", "topic": "Stool findings"},
        ]
        self.assertEqual(filter_card_indices(cards, query="blood", topic="All"), [0])
        self.assertEqual(filter_card_indices(cards, query="", topic="Stool findings"), [1])

    def test_sort_due_first(self):
        cards = [
            {"id": "a", "front": "A", "back": "B"},
            {"id": "b", "front": "C", "back": "D"},
        ]
        progress = {
            "a": {"due_timestamp": 50.0},
            "b": {"due_timestamp": 150.0},
        }
        ordered = sort_due_first([0, 1], cards, progress, now_ts=100.0)
        self.assertEqual(ordered, [0, 1])

    def test_validate_deck_schema(self):
        ok, _ = validate_deck_schema(
            {
                "name": "Demo",
                "cards": [{"front": "Q", "back": "A", "topic": "General"}],
            }
        )
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()

