from __future__ import annotations

import importlib
import random

from medical_decks import MEDICAL_DECKS

_pyscript = None
try:
    _pyscript = importlib.import_module("pyscript")
except ModuleNotFoundError:
    _pyscript = None


if _pyscript is not None:
    document = _pyscript.document
    when = _pyscript.when

    deck_name = next(iter(MEDICAL_DECKS))
    deck = MEDICAL_DECKS[deck_name]

    learn_index = 0
    learn_revealed = False

    practice_queue: list[int] = []
    current_index: int | None = None
    practice_asked = 0
    practice_correct = 0

    def _set_text(element_id: str, text: str) -> None:
        document.querySelector(element_id).textContent = text

    def _clear_children(element_id: str) -> None:
        parent = document.querySelector(element_id)
        while parent.firstChild is not None:
            parent.removeChild(parent.firstChild)

    def _set_card_side_label() -> None:
        side_text = "Front (Question)" if not learn_revealed else "Back (Answer)"
        _set_text("#learn-side", side_text)

    def _render_deck_selector() -> None:
        select = document.querySelector("#deck-select")
        _clear_children("#deck-select")
        for name in MEDICAL_DECKS.keys():
            option = document.createElement("option")
            option.value = name
            option.textContent = name
            if name == deck_name:
                option.selected = True
            select.appendChild(option)

    def _start_practice() -> None:
        state = globals()
        state["practice_queue"] = list(range(len(deck)))
        random.shuffle(state["practice_queue"])
        state["current_index"] = state["practice_queue"].pop() if state["practice_queue"] else None
        state["practice_asked"] = 0
        state["practice_correct"] = 0

    def _set_active_deck(selected_name: str) -> None:
        state = globals()
        state["deck_name"] = selected_name
        state["deck"] = MEDICAL_DECKS[selected_name]
        state["learn_index"] = 0
        state["learn_revealed"] = False
        _start_practice()

        _set_text("#practice-result", "")
        _set_text("#deck-status", f"{deck_name} - {len(deck)} cards")
        refresh_learn_view()
        refresh_practice_view()

    def refresh_learn_view() -> None:
        _set_card_side_label()
        _set_text("#learn-position", f"Card {learn_index + 1} of {len(deck)}")

        card = deck[learn_index]
        if learn_revealed:
            _set_text("#learn-card", card["back"])
            _set_text("#learn-reveal", "Show Question")
        else:
            _set_text("#learn-card", card["front"])
            _set_text("#learn-reveal", "Reveal Answer")

    def _get_practice_options(correct_answer: str) -> list[str]:
        pool = [entry["back"] for entry in deck if entry["back"] != correct_answer]
        random.shuffle(pool)
        options = [correct_answer] + pool[:3]
        random.shuffle(options)
        return options

    def refresh_practice_view() -> None:
        _clear_children("#practice-options")

        if current_index is None:
            _set_text("#practice-prompt", "Practice complete")
            _set_text("#practice-progress", f"Final score: {practice_correct}/{practice_asked}")
            return

        card = deck[current_index]
        _set_text("#practice-prompt", f"Pick the best answer: {card['front']}")
        _set_text(
            "#practice-progress",
            f"Score {practice_correct}/{practice_asked} | Remaining {len(practice_queue) + 1}",
        )

        options_parent = document.querySelector("#practice-options")
        for option in _get_practice_options(card["back"]):
            button = document.createElement("button")
            button.className = "option-btn"
            button.textContent = option
            button.setAttribute("data-answer", option)
            options_parent.appendChild(button)

    @when("change", "#deck-select")
    def on_deck_change(event):
        selected = document.querySelector("#deck-select").value
        _set_active_deck(selected)

    @when("click", "#learn-reveal")
    def on_learn_reveal(event):
        state = globals()
        state["learn_revealed"] = not state["learn_revealed"]
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

    @when("click", "#practice-options")
    def on_practice_choice(event):
        target = event.target
        if target.tagName.upper() != "BUTTON":
            return

        state = globals()
        if state["current_index"] is None:
            return

        selected_answer = target.getAttribute("data-answer")
        correct_answer = deck[state["current_index"]]["back"]

        state["practice_asked"] += 1
        if selected_answer == correct_answer:
            state["practice_correct"] += 1
            _set_text("#practice-result", "Correct")
        else:
            _set_text("#practice-result", f"Incorrect. Correct answer: {correct_answer}")

        state["current_index"] = state["practice_queue"].pop() if state["practice_queue"] else None
        refresh_practice_view()

    @when("click", "#practice-reset")
    def on_practice_reset(event):
        _start_practice()
        _set_text("#practice-result", "")
        refresh_practice_view()

    _render_deck_selector()
    _set_active_deck(deck_name)

