from __future__ import annotations

import importlib
import re

_pyscript = None
try:
    _pyscript = importlib.import_module("pyscript")
except ModuleNotFoundError:
    _pyscript = None


if _pyscript is not None:
    document = _pyscript.document
    when = _pyscript.when

    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]

    rank_aliases = {"ace": "a", "jack": "j", "queen": "q", "king": "k"}
    suit_aliases = {
        "c": "clubs",
        "club": "clubs",
        "clubs": "clubs",
        "d": "diamonds",
        "diamond": "diamonds",
        "diamonds": "diamonds",
        "h": "hearts",
        "heart": "hearts",
        "hearts": "hearts",
        "s": "spades",
        "spade": "spades",
        "spades": "spades",
    }

    learn_index = 0
    learn_revealed = False
    practice_queue = list(range(len(deck)))
    current_index = practice_queue.pop() if practice_queue else None

    def normalize_card_input(value: str) -> str:
        cleaned = " ".join(value.strip().lower().replace("-", " ").split())
        if " of " in cleaned:
            rank_raw, suit_raw = cleaned.split(" of ", 1)
            return f"{rank_aliases.get(rank_raw, rank_raw)} of {suit_aliases.get(suit_raw, suit_raw)}"

        match = re.fullmatch(
            r"(10|[2-9]|[ajqk]|ace|jack|queen|king)\s*([cdhs]|clubs?|diamonds?|hearts?|spades?)",
            cleaned,
        )
        if match:
            rank_raw, suit_raw = match.groups()
            return f"{rank_aliases.get(rank_raw, rank_raw)} of {suit_aliases.get(suit_raw, suit_raw)}"

        return cleaned

    def _set_text(element_id: str, text: str) -> None:
        document.querySelector(element_id).textContent = text

    def refresh_learn_view() -> None:
        _set_text("#learn-position", f"Card {learn_index + 1} / {len(deck)}")
        if learn_revealed:
            _set_text("#learn-card", deck[learn_index])
        else:
            _set_text("#learn-card", "Click Reveal to see the card")

    def refresh_practice_view() -> None:
        if current_index is None:
            _set_text("#practice-prompt", "Deck complete. Great work!")
            _set_text("#practice-progress", f"Progress: {len(deck)}/{len(deck)}")
            return

        asked = len(deck) - len(practice_queue)
        _set_text("#practice-prompt", f"What card is in position {current_index + 1}?")
        _set_text("#practice-progress", f"Progress: {asked}/{len(deck)}")

    @when("click", "#learn-reveal")
    def on_learn_reveal(event):
        nonlocal_learn_revealed = globals()
        nonlocal_learn_revealed["learn_revealed"] = True
        refresh_learn_view()

    @when("click", "#learn-next")
    def on_learn_next(event):
        state = globals()
        state["learn_index"] = (state["learn_index"] + 1) % len(deck)
        state["learn_revealed"] = False
        refresh_learn_view()

    @when("click", "#learn-prev")
    def on_learn_prev(event):
        state = globals()
        state["learn_index"] = (state["learn_index"] - 1) % len(deck)
        state["learn_revealed"] = False
        refresh_learn_view()

    @when("click", "#practice-submit")
    def on_practice_submit(event):
        state = globals()
        if state["current_index"] is None:
            return

        guess_input = document.querySelector("#guess")
        guess = guess_input.value
        expected = deck[state["current_index"]]
        is_correct = normalize_card_input(guess) == normalize_card_input(expected)
        if is_correct:
            _set_text("#practice-result", "Correct!")
        else:
            _set_text("#practice-result", f"Not quite. Correct answer: {expected}")

        guess_input.value = ""
        state["current_index"] = state["practice_queue"].pop() if state["practice_queue"] else None
        refresh_practice_view()

    @when("click", "#practice-reset")
    def on_practice_reset(event):
        state = globals()
        state["practice_queue"] = list(range(len(deck)))
        state["current_index"] = state["practice_queue"].pop() if state["practice_queue"] else None
        _set_text("#practice-result", "")
        refresh_practice_view()

    refresh_learn_view()
    refresh_practice_view()
