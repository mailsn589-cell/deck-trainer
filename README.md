# Medical Deck Trainer (Python 3 + Web UI)

A static flashcard trainer for your medical notes with a true card-by-card workflow.

- **Learn Mode**: one card at a time (question on front, answer on reveal).
- **Practice Mode**: multiple-choice recall with score tracking.
- **Deck Selector**: switch between `Abdomen and GI` and `Rectum and Genitourinary`.

## Project files

- `index.html` - page structure
- `styles.css` - responsive UI styling
- `deck_trainer.py` - browser-side study logic (PyScript) with embedded deck data for GitHub Pages reliability
- `medical_decks.py` - shared deck data for Python-side tests/reference
- `deck_logic.py` - helper logic + existing unit tests
- `main.py` - local static server
- `tests/test_deck_logic.py` - current unit tests
- `tests/test_medical_decks.py` - data integrity tests for medical decks

## Run locally

```powershell
python main.py
```

Then open `http://127.0.0.1:8000`.

## Run tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Add more cards in future

1. Open `medical_decks.py`.
2. Add cards under the target deck in this format:
   - `{"front": "Question or term", "back": "Answer or definition"}`
3. Save, commit, and push.
4. Refresh GitHub Pages after deployment.

## Deploy to GitHub Pages

1. Push to your repository `main` branch.
2. In repository settings, open **Pages**.
3. Source: `Deploy from a branch`, branch `main`, folder `/ (root)`.
4. Leave **Custom domain** empty unless you own a separate domain.

## If the live page still shows old cards

GitHub Pages and browser caching can delay updates. Do a hard refresh after push:

- Windows: `Ctrl + F5`
- macOS: `Cmd + Shift + R`

Also check that your latest commit includes changes to `index.html`, `deck_trainer.py`, `styles.css`, and `medical_decks.py`.

## PyScript import note

GitHub Pages runs PyScript in the browser (Pyodide). Local Python module imports can fail there unless explicitly packaged for PyScript.
To avoid `ModuleNotFoundError` in the browser, `deck_trainer.py` keeps runtime deck data embedded.

