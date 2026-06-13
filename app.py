from __future__ import annotations

import csv
import os
import random
from functools import lru_cache
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, session


BASE_DIR = Path(__file__).resolve().parent
DECK_FILE = BASE_DIR / "data" / "date_night_cards.csv"
SESSION_REMAINING_KEY = "remaining_card_ids"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")


@lru_cache(maxsize=1)
def load_deck() -> tuple[dict[str, Any], ...]:
    """Load cards once from CSV and normalize the fields used by the UI."""
    cards: list[dict[str, Any]] = []

    with DECK_FILE.open(newline="", encoding="utf-8") as deck_file:
        reader = csv.DictReader(deck_file)
        for row in reader:
            cards.append(
                {
                    "id": int(row["ID"]),
                    "category": row["Category"].strip(),
                    "tone": row["Tone"].strip(),
                    "text": row["CardText"].strip(),
                }
            )

    if not cards:
        raise RuntimeError(f"No cards were found in {DECK_FILE}")

    return tuple(cards)


def card_by_id(card_id: int) -> dict[str, Any]:
    for card in load_deck():
        if card["id"] == card_id:
            return card
    raise KeyError(card_id)


def all_card_ids() -> list[int]:
    return [card["id"] for card in load_deck()]


def reset_remaining_cards() -> list[int]:
    remaining_ids = all_card_ids()
    session[SESSION_REMAINING_KEY] = remaining_ids
    session.modified = True
    return remaining_ids


def get_remaining_cards() -> list[int]:
    remaining_ids = session.get(SESSION_REMAINING_KEY)
    valid_ids = set(all_card_ids())

    if (
        not isinstance(remaining_ids, list)
        or any(not isinstance(card_id, int) or card_id not in valid_ids for card_id in remaining_ids)
    ):
        return reset_remaining_cards()

    return remaining_ids


@app.get("/")
def index():
    remaining_ids = get_remaining_cards()
    total_cards = len(load_deck())

    return render_template(
        "index.html",
        remaining_count=len(remaining_ids),
        total_cards=total_cards,
    )


@app.post("/draw")
def draw_card():
    remaining_ids = get_remaining_cards()
    total_cards = len(load_deck())

    if not remaining_ids:
        return jsonify(
            {
                "card": None,
                "remaining": 0,
                "total": total_cards,
                "message": "The deck is empty. Refresh the deck to start again.",
            }
        )

    drawn_id = random.choice(remaining_ids)
    remaining_ids.remove(drawn_id)
    session[SESSION_REMAINING_KEY] = remaining_ids
    session.modified = True

    return jsonify(
        {
            "card": card_by_id(drawn_id),
            "remaining": len(remaining_ids),
            "total": total_cards,
            "message": None,
        }
    )


@app.post("/reset")
def reset_deck():
    remaining_ids = reset_remaining_cards()

    return jsonify(
        {
            "remaining": len(remaining_ids),
            "total": len(load_deck()),
            "message": "Deck refreshed.",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
