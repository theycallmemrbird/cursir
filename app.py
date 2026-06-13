import os
import random

from flask import Flask, jsonify, render_template, session

from cards import CARDS, CARDS_BY_ID


ALL_CARD_IDS = [card["id"] for card in CARDS]


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
    )

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        ensure_deck()
        return render_template("index.html", total_cards=len(ALL_CARD_IDS))

    @app.get("/api/status")
    def status():
        remaining_ids = ensure_deck()
        drawn_ids = session.get("drawn_ids", [])
        return jsonify(
            {
                "remaining": len(remaining_ids),
                "drawn": len(drawn_ids),
                "total": len(ALL_CARD_IDS),
                "empty": len(remaining_ids) == 0,
            }
        )

    @app.post("/api/draw")
    def draw_card():
        remaining_ids = ensure_deck()
        drawn_ids = session.setdefault("drawn_ids", [])

        if not remaining_ids:
            return jsonify(
                {
                    "card": None,
                    "remaining": 0,
                    "drawn": len(drawn_ids),
                    "total": len(ALL_CARD_IDS),
                    "empty": True,
                    "message": "The deck is empty. Refresh the deck to play again.",
                }
            )

        card_index = random.randrange(len(remaining_ids))
        card_id = remaining_ids.pop(card_index)
        drawn_ids.append(card_id)
        session["remaining_ids"] = remaining_ids
        session["drawn_ids"] = drawn_ids
        session.modified = True

        return jsonify(
            {
                "card": CARDS_BY_ID[card_id],
                "remaining": len(remaining_ids),
                "drawn": len(drawn_ids),
                "total": len(ALL_CARD_IDS),
                "empty": False,
            }
        )

    @app.post("/api/reset")
    def reset_deck():
        session["remaining_ids"] = ALL_CARD_IDS.copy()
        session["drawn_ids"] = []
        session.modified = True
        return jsonify(
            {
                "remaining": len(ALL_CARD_IDS),
                "drawn": 0,
                "total": len(ALL_CARD_IDS),
                "empty": False,
                "message": "Deck refreshed.",
            }
        )

    return app


def ensure_deck():
    if "remaining_ids" not in session:
        session["remaining_ids"] = ALL_CARD_IDS.copy()
        session["drawn_ids"] = []
        session.modified = True
    return session["remaining_ids"]


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
