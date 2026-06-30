from __future__ import annotations

import re
from typing import Any, Iterable

SECONDS_PER_DAY = 86400.0


def validate_deck_schema(deck_data: dict[str, Any]) -> tuple[bool, str]:
    if not isinstance(deck_data, dict):
        return False, "Deck must be an object"
    if not isinstance(deck_data.get("name"), str) or not deck_data["name"].strip():
        return False, "Deck name is required"

    cards = deck_data.get("cards")
    if not isinstance(cards, list) or not cards:
        return False, "Deck must include at least one card"

    for idx, card in enumerate(cards):
        if not isinstance(card, dict):
            return False, f"Card {idx} is not an object"
        if not isinstance(card.get("front"), str) or not card["front"].strip():
            return False, f"Card {idx} missing front"
        if not isinstance(card.get("back"), str) or not card["back"].strip():
            return False, f"Card {idx} missing back"
        if "topic" in card and not isinstance(card["topic"], str):
            return False, f"Card {idx} topic must be a string"

    return True, "ok"


def normalize_line(line: str) -> str:
    cleaned = line.replace("\u2022", "-").replace("\u25aa", "-")
    return re.sub(r"\s+", " ", cleaned).strip()


def looks_like_heading(line: str) -> bool:
    if len(line) > 70:
        return False
    if line.endswith(":"):
        return True
    words = line.split()
    return 1 <= len(words) <= 8 and all(w[:1].isupper() for w in words if w[:1].isalpha())


def parse_lines_to_cards(lines: Iterable[str], default_topic: str = "General") -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    current_topic = default_topic
    current_term = ""
    current_points: list[str] = []

    def flush_current() -> None:
        nonlocal current_term, current_points
        if current_term and current_points:
            cards.append({"front": current_term, "back": " ".join(current_points), "topic": current_topic})
        current_term = ""
        current_points = []

    normalized = [normalize_line(v) for v in lines]

    for line in normalized:
        if not line or re.fullmatch(r"\d+", line):
            continue

        qa_match = re.match(r"^([^:]{2,80}):\s+(.+)$", line)
        if qa_match:
            flush_current()
            cards.append(
                {
                    "front": qa_match.group(1).strip(),
                    "back": qa_match.group(2).strip(),
                    "topic": current_topic,
                }
            )
            continue

        if looks_like_heading(line):
            flush_current()
            current_topic = line.rstrip(":")
            continue

        if line.startswith("-"):
            bullet_text = line.lstrip("- ").strip()
            if current_term:
                current_points.append(bullet_text)
            else:
                cards.append({"front": f"{current_topic} note {len(cards) + 1}", "back": bullet_text, "topic": current_topic})
            continue

        if current_term:
            current_points.append(line)
        else:
            current_term = line

    flush_current()

    if cards:
        return cards

    compact = [line for line in normalized if line]
    for idx in range(0, len(compact), 2):
        front = compact[idx]
        back = compact[idx + 1] if idx + 1 < len(compact) else "Review this concept"
        cards.append({"front": front, "back": back, "topic": current_topic})

    return cards


def register_manifest_entry(manifest_data: dict[str, Any], deck_name: str, file_name: str) -> dict[str, Any]:
    result = dict(manifest_data)
    decks = list(result.get("decks", []))

    updated = False
    for entry in decks:
        if entry.get("file") == file_name:
            entry["name"] = deck_name
            updated = True
            break

    if not updated:
        decks.append({"name": deck_name, "file": file_name})

    result["decks"] = decks
    return result


def default_progress() -> dict[str, float | int | None]:
    return {
        "ease": 2.5,
        "interval_days": 0.0,
        "due_timestamp": 0.0,
        "last_reviewed": None,
        "streak": 0,
    }


def schedule_next(progress: dict[str, float | int | None], rating: str, now_ts: float) -> dict[str, float | int | None]:
    rating_key = rating.strip().lower()
    state = dict(progress)

    ease = float(state.get("ease", 2.5))
    interval = float(state.get("interval_days", 0.0))
    streak = int(state.get("streak", 0) or 0)

    if rating_key == "again":
        ease = max(1.3, ease - 0.2)
        interval = 5.0 / 1440.0
        streak = 0
    elif rating_key == "hard":
        ease = max(1.3, ease - 0.15)
        interval = max(1.0, interval * 1.2 if interval > 0 else 1.0)
        streak += 1
    elif rating_key == "good":
        interval = max(1.0, interval * ease if interval > 0 else 1.0)
        streak += 1
    elif rating_key == "easy":
        ease = min(3.5, ease + 0.15)
        interval = max(2.0, interval * ease * 1.3 if interval > 0 else 2.0)
        streak += 1
    else:
        raise ValueError(f"Unknown rating: {rating}")

    state["ease"] = round(ease, 3)
    state["interval_days"] = round(interval, 5)
    state["due_timestamp"] = now_ts + interval * SECONDS_PER_DAY
    state["last_reviewed"] = now_ts
    state["streak"] = streak
    return state


def filter_card_indices(cards: list[dict[str, str]], query: str = "", topic: str = "All") -> list[int]:
    q = query.strip().lower()
    t = topic.strip().lower()
    results: list[int] = []

    for idx, card in enumerate(cards):
        if t and t != "all":
            topic_value = str(card.get("topic", "General")).lower()
            if topic_value != t:
                continue
        if q:
            haystack = f"{card.get('front', '')} {card.get('back', '')}".lower()
            if q not in haystack:
                continue
        results.append(idx)
    return results


def sort_due_first(indices: list[int], cards: list[dict[str, str]], progress_map: dict[str, dict[str, float | int | None]], now_ts: float) -> list[int]:
    def sort_key(idx: int) -> tuple[int, float]:
        card_id = cards[idx].get("id", str(idx))
        due = float(progress_map.get(card_id, {}).get("due_timestamp", 0.0) or 0.0)
        is_future = 1 if due > now_ts else 0
        return is_future, due

    return sorted(indices, key=sort_key)
