# Deck Trainer (Python 3 + Web UI)

A flashcard-style trainer with two study modes using the medical content you provided.

- **Learn Mode**: read the prompt and reveal the answer.
- **Practice Mode**: choose the correct answer from multiple options.
- **Deck Selector**: switch between `Abdomen and GI` and `Rectum and Genitourinary`.

The interface is static and can be hosted with **GitHub Pages**.

## Project files

- `index.html` - web interface entry point
- `styles.css` - UI styles
- `deck_trainer.py` - browser-side Python handlers and deck data (PyScript)
- `deck_logic.py` - helper logic and unit-test target
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

## Add more cards in future

1. Open `deck_trainer.py`.
2. Add a new deck inside `DECKS` (same `{"front": ..., "back": ...}` format).
3. Save, commit, and push to GitHub.
4. GitHub Pages updates automatically after deployment.

## Host on GitHub Pages

1. Push this repository to GitHub.
2. In repository settings, open **Pages**.
3. Set source to branch `main` and folder `/ (root)`.
4. Keep **Custom domain** empty unless you own a separate domain.

Because the app is static, no backend hosting is needed.
