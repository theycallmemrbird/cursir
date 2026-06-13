# Date Night Card Draw

A small Flask app that draws one random card from a date-night deck when you
press the spacebar. Drawn cards stay out of the deck until you refresh it.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open <http://127.0.0.1:5000>, then press the spacebar or click **Draw Card**.

## Behavior

- Each browser session gets its own remaining deck.
- Drawing removes that card from the session's deck.
- **Refresh Deck** puts all cards back into the session's deck.
- When the deck is empty, no more cards are drawn until it is refreshed.
