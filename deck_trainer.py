from __future__ import annotations

import importlib
import json
import random
import time

_pyscript = None
try:
    _pyscript = importlib.import_module("pyscript")
except ModuleNotFoundError:
    _pyscript = None


if _pyscript is not None:
    document = _pyscript.document
    when = _pyscript.when

    _js = None
    try:
        _js = importlib.import_module("js")
    except ModuleNotFoundError:
        _js = None

    FALLBACK_DECKS = {
        "Abdomen and GI": [
            {"front": "Hematemesis", "back": "Vomiting blood; if exposed to gastric acid it may look like coffee grounds.", "topic": "Symptoms"},
            {"front": "Dysphagia", "back": "Difficulty swallowing.", "topic": "Symptoms"},
            {"front": "Odynophagia", "back": "Painful swallowing.", "topic": "Symptoms"},
            {"front": "Melena", "back": "Dark, tarry stool from upper GI bleeding.", "topic": "Stool findings"},
            {"front": "Hematochezia", "back": "Bright red blood often from rectum, anus, or sigmoid.", "topic": "Stool findings"},
            {"front": "Steatorrhea", "back": "Fatty diarrheal stool.", "topic": "Stool findings"},
            {"front": "Colorectal screening age", "back": "Routine screening is recommended around age 50, earlier if high risk.", "topic": "Screening"},
            {"front": "Diet advice", "back": "Balanced high-fiber diet and about 8 to 10 glasses of water per day.", "topic": "Prevention"},
        ],
        "Rectum and Genitourinary": [
            {"front": "Kidney functions", "back": "Maintain fluid and electrolyte balance, support red blood cell production, and filter waste.", "topic": "Anatomy"},
            {"front": "Ureters", "back": "Transport urine from kidneys to bladder.", "topic": "Anatomy"},
            {"front": "Bladder role", "back": "Stores urine; urge to void commonly appears near 300 mL.", "topic": "Anatomy"},
            {"front": "Urinary retention", "back": "Inability to empty the bladder.", "topic": "Urinary symptoms"},
            {"front": "Urinary hesitancy", "back": "Trouble starting urination.", "topic": "Urinary symptoms"},
            {"front": "Cystocele", "back": "Bladder prolapse into vagina with pressure or stress incontinence.", "topic": "Pelvic findings"},
            {"front": "Rectocele", "back": "Rectal prolapse into vagina with pressure and possible constipation.", "topic": "Pelvic findings"},
            {"front": "Paraphimosis", "back": "Retracted foreskin trapped behind glans; this is a medical emergency.", "topic": "Male findings"},
        ],
    }

    def _slug(value: str) -> str:
        return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")

    def _safe_json_get(path: str):
        if _js is None:
            return None
        try:
            xhr = _js.XMLHttpRequest.new()
            xhr.open("GET", path, False)
            xhr.send(None)
            if xhr.status == 200:
                return json.loads(str(xhr.responseText))
        except Exception:
            return None
        return None

    def _normalize_loaded_decks(raw_decks: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, str]]]:
        normalized: dict[str, list[dict[str, str]]] = {}
        for deck_name, cards in raw_decks.items():
            normalized_cards: list[dict[str, str]] = []
            for idx, card in enumerate(cards):
                front = str(card.get("front", "")).strip()
                back = str(card.get("back", "")).strip()
                if not front or not back:
                    continue
                topic = str(card.get("topic", "General")).strip() or "General"
                normalized_cards.append(
                    {
                        "id": str(card.get("id", f"{_slug(deck_name)}_{idx}")),
                        "front": front,
                        "back": back,
                        "topic": topic,
                    }
                )
            if normalized_cards:
                normalized[deck_name] = normalized_cards
        return normalized

    def _load_runtime_decks() -> tuple[dict[str, list[dict[str, str]]], str]:
        manifest = _safe_json_get("decks/manifest.json")
        if not manifest or not isinstance(manifest.get("decks"), list):
            return _normalize_loaded_decks(FALLBACK_DECKS), "fallback"

        loaded: dict[str, list[dict[str, str]]] = {}
        for item in manifest["decks"]:
            file_name = str(item.get("file", "")).strip()
            if not file_name:
                continue
            deck_data = _safe_json_get(f"decks/{file_name}")
            if not deck_data:
                continue
            deck_name = str(deck_data.get("name") or item.get("name") or "").strip()
            cards = deck_data.get("cards", [])
            if deck_name and isinstance(cards, list):
                loaded[deck_name] = cards

        if loaded:
            return _normalize_loaded_decks(loaded), "json"
        return _normalize_loaded_decks(FALLBACK_DECKS), "fallback"

    RUNTIME_DECKS, runtime_source = _load_runtime_decks()

    deck_name = next(iter(RUNTIME_DECKS))
    deck = RUNTIME_DECKS[deck_name]

    search_query = ""
    topic_filter = "All"

    learn_indices: list[int] = []
    learn_cursor = 0
    learn_revealed = False

    practice_queue: list[int] = []
    current_practice_index: int | None = None
    practice_asked = 0
    practice_correct = 0
    current_streak = 0

    progress_map: dict[str, dict[str, float | int | None]] = {}

    def _default_progress() -> dict[str, float | int | None]:
        return {
            "ease": 2.5,
            "interval_days": 0.0,
            "due_timestamp": 0.0,
            "last_reviewed": None,
            "streak": 0,
        }

    def _progress_key() -> str:
        return f"mdt_progress_{_slug(deck_name)}"

    def _save_progress() -> None:
        if _js is None:
            return
        try:
            _js.localStorage.setItem(_progress_key(), json.dumps(progress_map))
        except Exception:
            pass

    def _load_progress() -> None:
        state = globals()
        state["progress_map"] = {}
        if _js is None:
            return
        try:
            raw = _js.localStorage.getItem(_progress_key())
            if raw:
                parsed = json.loads(str(raw))
                if isinstance(parsed, dict):
                    state["progress_map"] = parsed
        except Exception:
            state["progress_map"] = {}

    def _get_progress(card_id: str) -> dict[str, float | int | None]:
        if card_id not in progress_map:
            progress_map[card_id] = _default_progress()
        return progress_map[card_id]

    def _set_text(selector: str, text: str) -> None:
        document.querySelector(selector).textContent = text

    def _clear_children(selector: str) -> None:
        parent = document.querySelector(selector)
        while parent.firstChild is not None:
            parent.removeChild(parent.firstChild)

    def _active_indices() -> list[int]:
        q = search_query.strip().lower()
        t = topic_filter.strip().lower()
        indices: list[int] = []
        for idx, card in enumerate(deck):
            if t != "all" and card.get("topic", "General").lower() != t:
                continue
            if q:
                haystack = f"{card['front']} {card['back']}".lower()
                if q not in haystack:
                    continue
            indices.append(idx)
        return indices

    def _sort_due_first(indices: list[int]) -> list[int]:
        now = time.time()

        def key(idx: int) -> tuple[int, float]:
            card_id = deck[idx]["id"]
            due = float(_get_progress(card_id).get("due_timestamp", 0.0) or 0.0)
            return (1 if due > now else 0, due)

        return sorted(indices, key=key)

    def _rebuild_topic_filter() -> None:
        select = document.querySelector("#topic-filter")
        _clear_children("#topic-filter")
        topics = sorted({card.get("topic", "General") for card in deck})
        for name in ["All", *topics]:
            option = document.createElement("option")
            option.value = name
            option.textContent = name
            if name == topic_filter:
                option.selected = True
            select.appendChild(option)

    def _render_deck_selector() -> None:
        select = document.querySelector("#deck-select")
        _clear_children("#deck-select")
        for name in RUNTIME_DECKS.keys():
            option = document.createElement("option")
            option.value = name
            option.textContent = name
            if name == deck_name:
                option.selected = True
            select.appendChild(option)

    def _schedule_next(card_state: dict[str, float | int | None], rating: str) -> dict[str, float | int | None]:
        now = time.time()
        state = dict(card_state)
        ease = float(state.get("ease", 2.5))
        interval = float(state.get("interval_days", 0.0))
        streak = int(state.get("streak", 0) or 0)

        if rating == "again":
            ease = max(1.3, ease - 0.2)
            interval = 5.0 / 1440.0
            streak = 0
        elif rating == "hard":
            ease = max(1.3, ease - 0.15)
            interval = max(1.0, interval * 1.2 if interval > 0 else 1.0)
            streak += 1
        elif rating == "good":
            interval = max(1.0, interval * ease if interval > 0 else 1.0)
            streak += 1
        else:
            ease = min(3.5, ease + 0.15)
            interval = max(2.0, interval * ease * 1.3 if interval > 0 else 2.0)
            streak += 1

        state["ease"] = round(ease, 3)
        state["interval_days"] = round(interval, 5)
        state["due_timestamp"] = now + interval * 86400.0
        state["last_reviewed"] = now
        state["streak"] = streak
        return state

    def _rebuild_indices_and_progress() -> None:
        state = globals()
        filtered = _active_indices()
        if not filtered:
            state["learn_indices"] = []
            state["learn_cursor"] = 0
            state["practice_queue"] = []
            state["current_practice_index"] = None
            return

        ordered = _sort_due_first(filtered)
        state["learn_indices"] = ordered
        if state["learn_cursor"] >= len(ordered):
            state["learn_cursor"] = 0

        now = time.time()
        due = [idx for idx in ordered if float(_get_progress(deck[idx]["id"]).get("due_timestamp", 0.0) or 0.0) <= now]
        future = [idx for idx in ordered if idx not in due]
        random.shuffle(future)
        queue = due + future
        state["practice_queue"] = queue
        state["current_practice_index"] = queue.pop(0) if queue else None

    def _refresh_progress_stats() -> None:
        now = time.time()
        active = _active_indices()
        due_count = 0
        for idx in active:
            due_ts = float(_get_progress(deck[idx]["id"]).get("due_timestamp", 0.0) or 0.0)
            if due_ts <= now:
                due_count += 1

        reviewed = 0
        for value in progress_map.values():
            if value.get("last_reviewed") is not None:
                reviewed += 1

        _set_text("#due-count", f"Due: {due_count}")
        _set_text("#reviewed-count", f"Reviewed: {reviewed}")
        _set_text("#streak-count", f"Streak: {current_streak}")

    def _refresh_filter_status() -> None:
        _set_text("#filter-status", f"Active filter: topic={topic_filter}, query='{search_query or '*'}', matches={len(_active_indices())}")

    def refresh_learn_view() -> None:
        _refresh_progress_stats()
        _refresh_filter_status()

        if not learn_indices:
            _set_text("#learn-side", "No cards")
            _set_text("#learn-position", "0 of 0")
            _set_text("#learn-card", "No cards match the current filter.")
            return

        card_idx = learn_indices[learn_cursor]
        card = deck[card_idx]

        _set_text("#learn-side", "Back (Answer)" if learn_revealed else "Front (Question)")
        _set_text("#learn-position", f"Card {learn_cursor + 1} of {len(learn_indices)}")
        _set_text("#learn-card", card["back"] if learn_revealed else card["front"])
        _set_text("#learn-reveal", "Show Question" if learn_revealed else "Reveal Answer")

    def _practice_options(correct_answer: str) -> list[str]:
        pool = [card["back"] for card in deck if card["back"] != correct_answer]
        random.shuffle(pool)
        options = [correct_answer] + pool[:3]
        random.shuffle(options)
        return options

    def refresh_practice_view() -> None:
        _clear_children("#practice-options")

        if current_practice_index is None:
            _set_text("#practice-prompt", "Practice complete")
            _set_text("#practice-progress", f"Score {practice_correct}/{practice_asked}")
            return

        card = deck[current_practice_index]
        _set_text("#practice-prompt", f"Pick the best answer: {card['front']}")
        _set_text("#practice-progress", f"Score {practice_correct}/{practice_asked} | Remaining {len(practice_queue) + 1}")

        parent = document.querySelector("#practice-options")
        for option in _practice_options(card["back"]):
            button = document.createElement("button")
            button.className = "option-btn"
            button.textContent = option
            button.setAttribute("data-answer", option)
            parent.appendChild(button)

    def _rate_learn_card(rating: str) -> None:
        state = globals()
        if not learn_indices:
            return

        card_idx = learn_indices[learn_cursor]
        card_id = deck[card_idx]["id"]
        state_data = _get_progress(card_id)
        progress_map[card_id] = _schedule_next(state_data, rating)
        _save_progress()

        if rating == "again":
            state["current_streak"] = 0
        else:
            state["current_streak"] += 1

        _rebuild_indices_and_progress()
        refresh_learn_view()
        refresh_practice_view()

    def _set_active_deck(selected_name: str) -> None:
        state = globals()
        state["deck_name"] = selected_name
        state["deck"] = RUNTIME_DECKS[selected_name]
        state["search_query"] = ""
        state["topic_filter"] = "All"
        state["learn_cursor"] = 0
        state["learn_revealed"] = False
        state["practice_asked"] = 0
        state["practice_correct"] = 0
        state["current_streak"] = 0

        document.querySelector("#search-input").value = ""
        _rebuild_topic_filter()
        _load_progress()
        _rebuild_indices_and_progress()
        _set_text("#practice-result", "")
        _set_text("#deck-status", f"{deck_name} - {len(deck)} cards (source: {runtime_source})")
        refresh_learn_view()
        refresh_practice_view()

    @when("change", "#deck-select")
    def on_deck_change(event):
        selected = document.querySelector("#deck-select").value
        _set_active_deck(selected)

    @when("change", "#topic-filter")
    def on_topic_filter(event):
        state = globals()
        state["topic_filter"] = document.querySelector("#topic-filter").value
        state["learn_cursor"] = 0
        state["learn_revealed"] = False
        _rebuild_indices_and_progress()
        refresh_learn_view()
        refresh_practice_view()

    @when("input", "#search-input")
    def on_search_input(event):
        state = globals()
        state["search_query"] = document.querySelector("#search-input").value
        state["learn_cursor"] = 0
        state["learn_revealed"] = False
        _rebuild_indices_and_progress()
        refresh_learn_view()
        refresh_practice_view()

    @when("click", "#clear-filters")
    def on_clear_filters(event):
        state = globals()
        state["search_query"] = ""
        state["topic_filter"] = "All"
        document.querySelector("#search-input").value = ""
        document.querySelector("#topic-filter").value = "All"
        _rebuild_indices_and_progress()
        refresh_learn_view()
        refresh_practice_view()

    @when("click", "#learn-reveal")
    def on_learn_reveal(event):
        state = globals()
        state["learn_revealed"] = not state["learn_revealed"]
        refresh_learn_view()

    @when("click", "#learn-next")
    def on_learn_next(event):
        state = globals()
        if not learn_indices:
            return
        state["learn_cursor"] = (learn_cursor + 1) % len(learn_indices)
        state["learn_revealed"] = False
        refresh_learn_view()

    @when("click", "#learn-prev")
    def on_learn_prev(event):
        state = globals()
        if not learn_indices:
            return
        state["learn_cursor"] = (learn_cursor - 1) % len(learn_indices)
        state["learn_revealed"] = False
        refresh_learn_view()

    @when("click", "#rate-again")
    def on_rate_again(event):
        _rate_learn_card("again")

    @when("click", "#rate-hard")
    def on_rate_hard(event):
        _rate_learn_card("hard")

    @when("click", "#rate-good")
    def on_rate_good(event):
        _rate_learn_card("good")

    @when("click", "#rate-easy")
    def on_rate_easy(event):
        _rate_learn_card("easy")

    @when("click", "#reset-progress")
    def on_reset_progress(event):
        state = globals()
        state["progress_map"] = {}
        state["current_streak"] = 0
        if _js is not None:
            _js.localStorage.removeItem(_progress_key())
        _rebuild_indices_and_progress()
        refresh_learn_view()
        refresh_practice_view()

    @when("click", "#practice-options")
    def on_practice_choice(event):
        target = event.target
        if target.tagName.upper() != "BUTTON" or current_practice_index is None:
            return

        state = globals()
        selected_answer = target.getAttribute("data-answer")
        correct_answer = deck[current_practice_index]["back"]

        state["practice_asked"] += 1
        if selected_answer == correct_answer:
            state["practice_correct"] += 1
            _set_text("#practice-result", "Correct")
            state["current_streak"] += 1
            card_id = deck[current_practice_index]["id"]
            progress_map[card_id] = _schedule_next(_get_progress(card_id), "good")
        else:
            _set_text("#practice-result", f"Incorrect. Correct answer: {correct_answer}")
            state["current_streak"] = 0
            card_id = deck[current_practice_index]["id"]
            progress_map[card_id] = _schedule_next(_get_progress(card_id), "again")

        _save_progress()
        state["current_practice_index"] = practice_queue.pop(0) if practice_queue else None
        refresh_practice_view()
        refresh_learn_view()

    @when("click", "#practice-reset")
    def on_practice_reset(event):
        state = globals()
        state["practice_asked"] = 0
        state["practice_correct"] = 0
        _rebuild_indices_and_progress()
        _set_text("#practice-result", "")
        refresh_practice_view()
        refresh_learn_view()

    _render_deck_selector()
    _set_active_deck(deck_name)

