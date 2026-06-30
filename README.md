# Deck Trainer (Python 3 + Web UI)

A flashcard-style deck trainer with two modes:
- **Learn Mode**: step through cards and reveal each answer.
- **Practice Mode**: guess the card at a prompted position and get instant feedback.

The interface is static and can be hosted with **GitHub Pages**.

## Project files

- `index.html` - web interface entry point
- `styles.css` - UI styles
- `deck_trainer.py` - browser-side Python handlers (PyScript)
- `deck_logic.py` - core deck/session logic shared with tests
- `main.py` - local static server runner
- `tests/test_deck_logic.py` - tiny test harness

## Run locally

```powershell
python main.py
```

Then open `http://127.0.0.1:8000`.

## Run tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Host on GitHub Pages

1. Push this repository to GitHub.
2. In repository settings, open **Pages**.
3. Set source to the root branch (`main` / `/root`).
4. Save, then open the provided Pages URL.

Because the app is static, no backend hosting is needed.

