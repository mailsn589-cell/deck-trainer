# Medical Deck Trainer (Python 3 + Web UI)

A static flashcard trainer for medical notes with deck filtering and spaced repetition.

## Features

- **Deck loading**: JSON-first from `decks/manifest.json` with embedded fallback if fetch fails.
- **Learn mode**: one card at a time, front/back reveal, next/previous navigation.
- **Spaced repetition**: `Again`, `Hard`, `Good`, `Easy` ratings with localStorage persistence.
- **Practice mode**: multiple-choice recall with score and progress.
- **Filters**: search by text and topic dropdown.
- **Deck creation tools**: local converters for PDF, PPTX, and raw text.

## Project files

- `index.html` - page structure and controls
- `styles.css` - responsive UI styles
- `deck_trainer.py` - browser-side logic and fallback decks (PyScript)
- `flashcard_core.py` - testable scheduler/filter/schema/helpers
- `medical_decks.py` - Python-side deck source used by tests
- `decks/manifest.json` - runtime deck registry
- `decks/*.json` - runtime deck files fetched by browser
- `scripts/pdf_to_deck.py` - local PDF-to-JSON converter
- `scripts/pptx_to_deck.py` - local PPTX-to-JSON converter
- `scripts/text_to_deck.py` - local raw-text-to-JSON converter
- `scripts/register_deck.py` - manifest update helper
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

## Create deck from PDF

```powershell
python scripts\pdf_to_deck.py --input "Abdomen-1.pdf" --output "decks\abdomen_from_pdf.json" --name "Abdomen From PDF"
```

## Create deck from PPTX

```powershell
python scripts\pptx_to_deck.py --input "slides.pptx" --output "decks\slides_deck.json" --name "Slides Deck"
```

## Create deck from raw text

```powershell
python scripts\text_to_deck.py --input-file "notes.txt" --output "decks\notes_deck.json" --name "Notes Deck"
python scripts\text_to_deck.py --input-string "Hematemesis: Vomiting blood" --output "decks\quick_deck.json" --name "Quick Deck"
```

## Register a new deck in manifest

```powershell
python scripts\register_deck.py --name "Slides Deck" --file "slides_deck.json"
```

## Verify new deck appears in app

1. Ensure the JSON file exists under `decks/`.
2. Ensure `decks/manifest.json` contains the deck file entry.
3. Run `python main.py` and open the app.
4. Confirm the deck appears in the `Deck` dropdown.

## Deploy to GitHub Pages

1. Push to `main`.
2. In repository settings, open **Pages**.
3. Source: `Deploy from a branch`, branch `main`, folder `/ (root)`.
4. Keep **Custom domain** empty unless you own one.

## Cache refresh note

After deployment, force reload the page to avoid stale assets:

- Windows: `Ctrl + F5`
- macOS: `Cmd + Shift + R`
