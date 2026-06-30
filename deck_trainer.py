from __future__ import annotations

import importlib
import random

MEDICAL_DECKS = {
    "Abdomen and GI": [
        {"front": "Hematemesis", "back": "Vomiting blood; if exposed to gastric acid it may look like coffee grounds."},
        {"front": "Dysphagia", "back": "Difficulty swallowing."},
        {"front": "Odynophagia", "back": "Painful swallowing."},
        {"front": "Aerophagia", "back": "Excessive flatus from swallowed air."},
        {"front": "Icterus (jaundice)", "back": "Associated with hepatitis, biliary cirrhosis, or gallstones."},
        {"front": "Anorexia", "back": "Loss of appetite."},
        {"front": "Melena", "back": "Dark, tarry stool from upper GI bleeding."},
        {"front": "Hematochezia", "back": "Bright red blood, often from rectum, anus, or sigmoid."},
        {"front": "Steatorrhea", "back": "Fatty diarrheal stool."},
        {"front": "Pale or clay stool", "back": "May indicate impaired biliary production or flow."},
        {"front": "Colorectal screening age", "back": "Routine screening is recommended around age 50, earlier if high risk."},
        {"front": "Exercise and constipation", "back": "Sedentary lifestyle increases constipation risk; walking 30 minutes daily helps."},
        {"front": "Diet advice for bowel health", "back": "Balanced high-fiber diet and about 8 to 10 glasses of water per day."},
        {"front": "Probiotics", "back": "Promote beneficial microorganisms in the GI tract."},
        {"front": "Meconium", "back": "First stool, usually passed in the first 24 to 48 hours."},
        {"front": "Gastrocolic reflex", "back": "Peristalsis is stimulated after eating."},
        {"front": "Umbilicus expected", "back": "Midline and usually inverted."},
        {"front": "Umbilicus unexpected", "back": "Redness, swelling, discoloration, or lesions are abnormal."},
        {"front": "Shape and contour expected", "back": "Flat, even, slightly convex, or rounded can be normal."},
        {"front": "Shape unexpected", "back": "Marked distention or severe concavity is abnormal."},
    ],
    "Rectum and Genitourinary": [
        {"front": "Kidney functions", "back": "Maintain fluid and electrolyte balance, support red blood cell production, and filter waste."},
        {"front": "Ureters", "back": "Transport urine from kidneys to bladder."},
        {"front": "Bladder role", "back": "Stores urine; urge to void commonly appears near 300 mL."},
        {"front": "Urethra role", "back": "Passageway for urine; in males it also carries semen."},
        {"front": "Urinary retention", "back": "Inability to empty the bladder."},
        {"front": "Urinary hesitancy", "back": "Trouble starting urination."},
        {"front": "Urinary urgency", "back": "Inability to wait to urinate."},
        {"front": "Dribbling", "back": "Leakage before or after full urinary stream."},
        {"front": "Nocturia", "back": "Urinating repeatedly during the night."},
        {"front": "Stress incontinence", "back": "Leakage with coughing, sneezing, or exertion."},
        {"front": "Goodell sign", "back": "Softening of the cervix around 4 to 6 weeks gestation."},
        {"front": "Chadwick sign", "back": "Cyanotic vaginal mucosa and cervix around 6 to 8 weeks gestation."},
        {"front": "Hegar sign", "back": "Softening of uterine isthmus around 4 to 6 weeks and into first trimester."},
        {"front": "Cystocele", "back": "Bladder prolapse into vagina with pressure or stress incontinence."},
        {"front": "Rectocele", "back": "Rectal prolapse into vagina with pressure and possible constipation."},
        {"front": "Hydrocele", "back": "Fluid collection around testicle causing usually painless swelling."},
        {"front": "Phimosis", "back": "Foreskin cannot retract over the glans."},
        {"front": "Paraphimosis", "back": "Retracted foreskin trapped behind glans; this is a medical emergency."},
        {"front": "Priapism", "back": "Painful prolonged erection unrelated to sexual arousal."},
        {"front": "Cryptorchidism", "back": "Undescended testes."},
    ],
}

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

