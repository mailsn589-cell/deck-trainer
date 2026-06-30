# Medical Deck Trainer (Python 3 + Web UI)

A static flashcard trainer for medical notes with deck filtering and spaced repetition.

## Features

- **Deck loading**: JSON-first from `decks/manifest.json` with embedded fallback if fetch fails.
- **Learn mode**: one card at a time, front/back reveal, next/previous navigation.
- **Spaced repetition**: `Again`, `Hard`, `Good`, `Easy` ratings with localStorage persistence.
- **Practice mode**: multiple-choice recall with score and progress.
- **Filters**: search by text and topic dropdown.

## Project files

- `index.html` - page structure and controls
- `styles.css` - responsive UI styles
- `deck_trainer.py` - browser-side logic and fallback decks (PyScript)
- `flashcard_core.py` - testable scheduler/filter/schema helpers
- `medical_decks.py` - Python-side deck source used by tests
- `decks/manifest.json` - runtime deck registry
- `decks/*.json` - runtime deck files fetched by browser
- `scripts/pdf_to_deck.py` - local PDF-to-JSON deck converter
- `main.py` - local static server
- `tests/` - unit tests

## Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run locally

```powershell
python main.py
```

Open `http://127.0.0.1:8000`.

## Run tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Convert PDF to deck JSON

```powershell
python scripts\pdf_to_deck.py --input "Abdomen-1.pdf" --output "decks\abdomen_from_pdf.json" --name "Abdomen From PDF"
python scripts\pdf_to_deck.py --input "Abdomen-1.pdf" --input "Rectum & Genitourinary-1.pdf" --output "decks\combined.json" --name "Combined Notes"
```

Then add the new deck file to `decks/manifest.json`.

## Add future PDFs in 4 steps

1. Run `scripts/pdf_to_deck.py` to create a new deck JSON file under `decks/`.
2. Register the file in `decks/manifest.json`.
3. Commit and push to GitHub.
4. Hard refresh the live site.

## Deploy to GitHub Pages

1. Push to `main`.
2. In repository settings, open **Pages**.
3. Source: `Deploy from a branch`, branch `main`, folder `/ (root)`.
4. Keep **Custom domain** empty unless you own one.

## Cache refresh note

After deployment, force reload the page to avoid stale assets:

- Windows: `Ctrl + F5`
- macOS: `Cmd + Shift + R`
