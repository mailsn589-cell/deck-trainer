from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
import re
from typing import List, Optional, Tuple

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]



def build_standard_deck() -> List[str]:
    """Return a standard 52-card deck in a deterministic order."""
    return [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]



def normalize_card_input(value: str) -> str:
    """Normalize user guesses so short forms and case differences still match."""
    cleaned = " ".join(value.strip().lower().replace("-", " ").split())

    rank_aliases = {
        "ace": "a",
        "jack": "j",
        "queen": "q",
        "king": "k",
    }
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

    # Format: "queen of hearts", "q of h", etc.
    if " of " in cleaned:
        rank_raw, suit_raw = cleaned.split(" of ", 1)
        rank_norm = rank_aliases.get(rank_raw, rank_raw)
        suit_norm = suit_aliases.get(suit_raw, suit_raw)
        return f"{rank_norm} of {suit_norm}"

    # Format: "qh", "10s", "queen hearts".
    match = re.fullmatch(
        r"(10|[2-9]|[ajqk]|ace|jack|queen|king)\s*([cdhs]|clubs?|diamonds?|hearts?|spades?)",
        cleaned,
    )
    if match:
        rank_raw, suit_raw = match.groups()
        rank_norm = rank_aliases.get(rank_raw, rank_raw)
        suit_norm = suit_aliases.get(suit_raw, suit_raw)
        return f"{rank_norm} of {suit_norm}"

    return cleaned


@dataclass
class LearnSession:
    deck: List[str] = field(default_factory=build_standard_deck)
    index: int = 0
    revealed: bool = False

    @property
    def total(self) -> int:
        return len(self.deck)

    def current_position(self) -> int:
        return self.index + 1

    def current_card(self) -> str:
        return self.deck[self.index]

    def reveal(self) -> str:
        self.revealed = True
        return self.current_card()

    def next_card(self) -> str:
        self.index = (self.index + 1) % self.total
        self.revealed = False
        return self.current_card()

    def prev_card(self) -> str:
        self.index = (self.index - 1) % self.total
        self.revealed = False
        return self.current_card()


@dataclass
class PracticeSession:
    deck: List[str] = field(default_factory=build_standard_deck)
    seed: Optional[int] = None
    asked_indices: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._rng = Random(self.seed)
        all_indices = list(range(len(self.deck)))
        self._rng.shuffle(all_indices)
        self._queue = all_indices
        self.current_index: Optional[int] = None

    @property
    def total(self) -> int:
        return len(self.deck)

    def next_prompt(self) -> Optional[Tuple[int, str]]:
        if not self._queue:
            self.current_index = None
            return None
        self.current_index = self._queue.pop()
        self.asked_indices.append(self.current_index)
        return self.current_index + 1, self.deck[self.current_index]

    def check_guess(self, guess: str) -> Tuple[bool, str]:
        if self.current_index is None:
            raise ValueError("No active prompt. Call next_prompt() first.")

        expected = self.deck[self.current_index]
        is_correct = normalize_card_input(guess) == normalize_card_input(expected)
        return is_correct, expected

    def progress(self) -> Tuple[int, int]:
        return len(self.asked_indices), self.total
