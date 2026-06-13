# Date Night Card Deck

A small Flask app that draws a random card from a deck when you press the
spacebar. Drawn cards stay out of the deck for the current browser session until
you refresh the deck.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open the local Flask URL in your browser, then press `Space` or use the
on-screen button to draw cards.

## Test

```bash
pytest
```
