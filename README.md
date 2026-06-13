# Date Night Card Deck

A small Flask app that draws a random card from a deck when you press the
spacebar. Drawn cards stay out of the deck for the current browser session until
you refresh the deck.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m flask --app app run
```

Open the local Flask URL in your browser, then press `Space` or use the
on-screen button to draw cards.

## Test

```bash
python3 -m pytest
```
