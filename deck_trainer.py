from __future__ import annotations

import importlib
import random

_pyscript = None
try:
    _pyscript = importlib.import_module("pyscript")
except ModuleNotFoundError:
    _pyscript = None


if _pyscript is not None:
    document = _pyscript.document
    when = _pyscript.when

    DECKS = {
        "Abdomen and GI": [
            {"front": "Hematemesis", "back": "Vomiting blood; if exposed to gastric acid it may look like coffee grounds."},
            {"front": "Dysphagia", "back": "Difficulty swallowing."},
            {"front": "Odynophagia", "back": "Painful swallowing."},
            {"front": "Aerophagia", "back": "Excessive flatus from swallowed air."},
            {"front": "Icterus (jaundice)", "back": "Associated with hepatitis, biliary cirrhosis, or gallstones."},
            {"front": "Anorexia", "back": "Loss of appetite."},
            {"front": "Expected skin finding (abdomen)", "back": "Skin should be smooth, dry, and even in tone (or lighter from less sun)."},
            {"front": "Unexpected skin findings", "back": "Bruising, dilated veins, rashes, or yellowing are concerning."},
            {"front": "Symmetry and masses expected", "back": "Abdominal movement should be symmetric with no masses."},
            {"front": "Symmetry unexpected", "back": "Localized bulging, mass, or asymmetric movement is abnormal."},
            {"front": "Shape and contour expected", "back": "Flat, even, slightly convex, or rounded can be normal."},
            {"front": "Shape variation in thin body frame", "back": "Scaphoid contour can be a normal variation."},
            {"front": "Shape variation in obese patients", "back": "Increased subcutaneous fat changes contour."},
            {"front": "Shape variation in older adults", "back": "Decreased muscle tone can change contour."},
            {"front": "Shape unexpected", "back": "Marked distention or severe concavity is abnormal."},
            {"front": "Umbilicus expected", "back": "Midline and usually inverted."},
            {"front": "Umbilicus variation", "back": "Piercing or mild extraversion may be a variation."},
            {"front": "Umbilicus unexpected", "back": "Redness, swelling, discoloration, or lesions are abnormal."},
            {"front": "Exercise and constipation", "back": "Sedentary lifestyle increases constipation risk; walking 30 minutes daily helps."},
            {"front": "Diet advice for bowel health", "back": "Balanced high-fiber diet and about 8 to 10 glasses of water per day."},
            {"front": "Colorectal screening age", "back": "Routine screening is recommended around age 50, earlier if high risk."},
            {"front": "Stool and scope testing", "back": "Check stool for blood; use sigmoidoscopy, colonoscopy, or barium enema."},
            {"front": "Probiotics", "back": "Promote beneficial microorganisms in the GI tract."},
            {"front": "Pediatric GI history: stool questions", "back": "Ask stool frequency, constipation, pain, and tolerance of new foods."},
            {"front": "Pediatric GI history: nutrition questions", "back": "Ask current diet, water intake, and infant feeding tolerance."},
            {"front": "Melena", "back": "Dark, tarry stool from upper GI bleeding."},
            {"front": "Tarry stool without melena", "back": "Iron can cause dark/tarry stool appearance."},
            {"front": "Black non-tarry stool causes", "back": "Pepto-Bismol, black licorice, or blueberries can darken stool."},
            {"front": "Hematochezia", "back": "Bright red blood, often from rectum, anus, or sigmoid."},
            {"front": "Red hematemesis", "back": "Vomiting fresh blood."},
            {"front": "Steatorrhea", "back": "Fatty diarrheal stool."},
            {"front": "Pale or clay stool", "back": "May indicate impaired biliary production/flow."},
            {"front": "Meconium", "back": "First stool, usually passed in the first 24 to 48 hours."},
            {"front": "Gastrocolic reflex", "back": "Peristalsis is stimulated after eating."},
            {"front": "Fecal occult blood testing", "back": "Common recommendation is yearly screening."},
            {"front": "Flexible sigmoidoscopy schedule", "back": "Often every 5 years with rectal exam."},
            {"front": "Double contrast barium enema schedule", "back": "Often every 5 years."},
            {"front": "Colonoscopy schedule", "back": "Often every 10 years for average risk screening."},
            {"front": "Abdominal percussion expected", "back": "Tympany predominates; dullness is expected over organs or stool."},
            {"front": "Abdominal pain triage question", "back": "Assess onset, location, radiation, timing, severity, and aggravating factors."},
        ],
        "Rectum and Genitourinary": [
            {"front": "Kidney functions", "back": "Maintain fluid/electrolyte balance, produce erythropoietic signals, and filter waste."},
            {"front": "Ureters", "back": "Transport urine from kidneys to bladder."},
            {"front": "Bladder role", "back": "Stores urine; urge to void commonly appears near 300 mL."},
            {"front": "Urethra role", "back": "Passageway for urine; in males also carries semen."},
            {"front": "Urinary retention", "back": "Inability to empty the bladder."},
            {"front": "Urinary hesitancy", "back": "Trouble starting urination."},
            {"front": "Urinary urgency", "back": "Inability to wait to urinate."},
            {"front": "Dribbling", "back": "Leakage before or after full urinary stream."},
            {"front": "Urinary frequency", "back": "Voiding more often than normal."},
            {"front": "Nocturia", "back": "Urinating repeatedly during the night."},
            {"front": "Incontinence", "back": "Loss of bladder control."},
            {"front": "Urge incontinence", "back": "Leakage related to sudden urge and poor control."},
            {"front": "Stress incontinence", "back": "Leakage with coughing, sneezing, or exertion."},
            {"front": "Nulliparous cervix", "back": "Typically smooth with a small circular os."},
            {"front": "Parous cervix", "back": "Os may be larger and more irregular after childbirth."},
            {"front": "Urinary interview basics", "back": "Ask about stream, urgency, frequency, pain, and foul odor."},
            {"front": "Anorectal interview basics", "back": "Ask about hemorrhoid symptoms, stool changes, blood/pus/mucus, and bowel routine."},
            {"front": "Reproductive interview basics", "back": "Ask nonjudgmentally about identity/practices, menstrual history, and exam frequency."},
            {"front": "Pelvic exam position", "back": "Supine, knees bent, feet supported; ensure privacy and comfort."},
            {"front": "Pelvic exam preparation", "back": "Client should void before exam; explain each step with gentle but firm technique."},
            {"front": "Mons pubis expected", "back": "Hair distribution varies but should be generally even; skin should be clear and even."},
            {"front": "Mons pubis unexpected", "back": "Swelling, redness, lesions, ulcerations, patchy hair loss, or pubic lice."},
            {"front": "Labia and vestibule expected", "back": "Usually symmetric, smooth, and darker in color than surrounding skin."},
            {"front": "Labia and vestibule unexpected", "back": "Inflammation, ulceration, malodorous discharge, tenderness, white patches, lumps."},
            {"front": "Cervical prolapse", "back": "Cervix descends toward vaginal opening from weakened pelvic support."},
            {"front": "Bartholin gland abscess", "back": "Fluid-filled infected pocket causing painful labial swelling."},
            {"front": "Cystocele", "back": "Bladder prolapse into vagina; pressure and stress incontinence can occur."},
            {"front": "Rectocele", "back": "Rectal prolapse into vagina; pressure and constipation can occur."},
            {"front": "Goodell sign", "back": "Softening of the cervix around 4 to 6 weeks gestation."},
            {"front": "Chadwick sign", "back": "Cyanotic vaginal mucosa/cervix around 6 to 8 weeks gestation."},
            {"front": "Hegar sign", "back": "Softening of uterine isthmus around 4 to 6 weeks and into first trimester."},
            {"front": "Pregnancy uterine capacity", "back": "Can increase about 500 to 1000 times during pregnancy."},
            {"front": "Mucus plug purpose", "back": "Protects fetus from infection; dislodging can cause a bloody show."},
            {"front": "Vaginal pH in pregnancy", "back": "More acidic from lactic acid, limiting bacterial growth but increasing candidiasis risk."},
            {"front": "Female puberty onset", "back": "Usually begins around ages 8 to 12, often with thelarche (breast budding)."},
            {"front": "Menopause", "back": "Permanent cessation of menses, often around age 48 to 51."},
            {"front": "Postmenopausal genital changes", "back": "Atrophy, reduced secretions, alkaline pH, and possible prolapse from muscle weakness."},
            {"front": "Male genital exam basics", "back": "Inspect penis, meatus, scrotum/testes, and inguinal region with respect and reassurance."},
            {"front": "Penis expected findings", "back": "Hairless shaft skin, visible dorsal vein, smooth glans, no lesions."},
            {"front": "Penis unexpected findings", "back": "Inflammation, ulcers, nodules, pubic lice, or nonretractile foreskin."},
            {"front": "Urethral meatus expected", "back": "Midline opening with smooth surrounding tissue."},
            {"front": "Hypospadias", "back": "Urethral meatus on ventral side of penis."},
            {"front": "Epispadias", "back": "Urethral meatus on dorsal side of penis."},
            {"front": "Scrotum and testes expected", "back": "Scrotum darker than skin, left testis often lower, testes similar size and mobile."},
            {"front": "Scrotum and testes unexpected", "back": "Edema, nodules, very small testes, or absent testis."},
            {"front": "Inguinal/femoral unexpected", "back": "Bulge or swelling can indicate hernia."},
            {"front": "External hemorrhoids", "back": "Dilated veins at anal opening, often from straining."},
            {"front": "Thrombosed hemorrhoid", "back": "Bluish-purple painful swelling caused by a clot."},
            {"front": "Rectal prolapse", "back": "Partial or complete protrusion of rectal wall through anal opening."},
            {"front": "Hydrocele", "back": "Fluid collection around testicle causing usually painless swelling."},
            {"front": "Peyronie disease", "back": "Fibrous plaque in penile tissue causing curvature, often after repeated injury."},
            {"front": "Genital warts", "back": "Usually caused by human papillomavirus (HPV)."},
            {"front": "Herpes simplex lesions", "back": "Typically present as painful vesicles."},
            {"front": "Cryptorchidism", "back": "Undescended testes."},
            {"front": "Circumcision", "back": "Removal of foreskin; may reduce STI/HPV/HIV risk and has cultural or religious context."},
            {"front": "Phimosis", "back": "Foreskin cannot retract over glans."},
            {"front": "Paraphimosis", "back": "Retracted foreskin trapped behind glans; medical emergency."},
            {"front": "Priapism", "back": "Painful prolonged erection unrelated to sexual arousal."},
            {"front": "Male puberty onset", "back": "Typically begins with testicular enlargement (gonadarche), around ages 9 to 14."},
            {"front": "Male aging urinary changes", "back": "Prostate hypertrophy can cause nocturia, weak stream, and urgency."},
            {"front": "Urinalysis key markers", "back": "Color, pH, specific gravity, BUN, and creatinine are common metrics."},
            {"front": "Acute urinary retention", "back": "Immediate emergency with painful urge, abdominal swelling, and inability to void."},
            {"front": "Chronic urinary retention", "back": "Frequency, hesitancy, intermittent stream, and post-void urgency over time."},
            {"front": "Pilonidal cyst", "back": "Hair-containing cyst over coccyx; may open as a dimple."},
            {"front": "Pilonidal dimple", "back": "Small dimple from incomplete vertebral closure; usually benign."},
            {"front": "Female screening", "back": "Pelvic exam and Pap screening typically from ages 21 to 65 per guideline intervals."},
            {"front": "Prostate cancer screening", "back": "PSA and digital rectal exam are used; risk-based timing applies."},
            {"front": "PSA pre-test instruction", "back": "Avoid ejaculation for 2 days before PSA testing."},
            {"front": "Testicular self-exam", "back": "Monthly self-check helps detect small movable lumps early."},
            {"front": "HPV vaccine", "back": "Gardasil protects against HPV-related cancers and is recommended before sexual activity."},
            {"front": "Hepatitis B vaccine", "back": "Recommended for exposure risk because Hep B spreads via bodily fluids."},
            {"front": "Contraception categories", "back": "Natural, barrier, pharmacologic, and surgical methods."},
            {"front": "HIV screening guidance", "back": "Screen ages 15 to 75 and during pregnancy; test high-risk clients at least annually."},
            {"front": "STI counseling", "back": "Use open-ended, nonjudgmental, age-appropriate education on risk and protection."},
            {"front": "Trauma-informed question", "back": "Ask gently about unwanted touching and identify trusted support people."},
        ],
    }

    deck_name = list(DECKS.keys())[0]
    deck = DECKS[deck_name]

    learn_index = 0
    learn_revealed = False

    practice_queue = []
    current_index = None
    practice_asked = 0
    practice_correct = 0

    def _set_text(element_id: str, text: str) -> None:
        document.querySelector(element_id).textContent = text

    def _clear_children(element_id: str) -> None:
        parent = document.querySelector(element_id)
        while parent.firstChild is not None:
            parent.removeChild(parent.firstChild)

    def _update_deck_status() -> None:
        _set_text("#deck-status", f"Loaded deck: {deck_name} ({len(deck)} cards)")

    def _reset_learn() -> None:
        state = globals()
        state["learn_index"] = 0
        state["learn_revealed"] = False

    def _start_practice() -> None:
        state = globals()
        state["practice_queue"] = list(range(len(deck)))
        random.shuffle(state["practice_queue"])
        state["current_index"] = state["practice_queue"].pop() if state["practice_queue"] else None
        state["practice_asked"] = 0
        state["practice_correct"] = 0

    def _set_active_deck(selected: str) -> None:
        state = globals()
        state["deck_name"] = selected
        state["deck"] = DECKS[selected]
        _reset_learn()
        _start_practice()
        _set_text("#practice-result", "")
        _update_deck_status()
        refresh_learn_view()
        refresh_practice_view()

    def _render_deck_selector() -> None:
        select = document.querySelector("#deck-select")
        _clear_children("#deck-select")
        for name in DECKS.keys():
            option = document.createElement("option")
            option.value = name
            option.textContent = name
            if name == deck_name:
                option.selected = True
            select.appendChild(option)

    def refresh_learn_view() -> None:
        _set_text("#learn-position", f"Card {learn_index + 1} / {len(deck)}")
        if learn_revealed:
            _set_text("#learn-card", deck[learn_index]["back"])
        else:
            _set_text("#learn-card", deck[learn_index]["front"])

    def _get_options(correct_answer: str) -> list[str]:
        incorrect = [card["back"] for card in deck if card["back"] != correct_answer]
        random.shuffle(incorrect)
        options = [correct_answer] + incorrect[:3]
        random.shuffle(options)
        return options

    def refresh_practice_view() -> None:
        _clear_children("#practice-options")

        if current_index is None:
            _set_text("#practice-prompt", "Deck complete. Great work!")
            _set_text(
                "#practice-progress",
                f"Score: {practice_correct}/{practice_asked} | Completed: {len(deck)}/{len(deck)}",
            )
            return

        card = deck[current_index]
        _set_text("#practice-prompt", f"Choose the best answer for: {card['front']}")
        _set_text(
            "#practice-progress",
            f"Score: {practice_correct}/{practice_asked} | Remaining: {len(practice_queue) + 1}",
        )

        options_parent = document.querySelector("#practice-options")
        for option_text in _get_options(card["back"]):
            button = document.createElement("button")
            button.className = "option-btn"
            button.textContent = option_text
            button.setAttribute("data-answer", option_text)
            options_parent.appendChild(button)

    @when("change", "#deck-select")
    def on_deck_change(event):
        select = document.querySelector("#deck-select")
        _set_active_deck(select.value)

    @when("click", "#learn-reveal")
    def on_learn_reveal(event):
        state = globals()
        state["learn_revealed"] = not state["learn_revealed"]
        refresh_learn_view()

    @when("click", "#learn-next")
    def on_learn_next(event):
        state = globals()
        state["learn_index"] = (state["learn_index"] + 1) % len(deck)
        state["learn_revealed"] = False
        refresh_learn_view()

    @when("click", "#learn-prev")
    def on_learn_prev(event):
        state = globals()
        state["learn_index"] = (state["learn_index"] - 1) % len(deck)
        state["learn_revealed"] = False
        refresh_learn_view()

    @when("click", "#practice-options")
    def on_practice_option(event):
        target = event.target
        if target.tagName != "BUTTON":
            return

        state = globals()
        if state["current_index"] is None:
            return

        selected = target.getAttribute("data-answer")
        correct = deck[state["current_index"]]["back"]

        state["practice_asked"] += 1
        if selected == correct:
            state["practice_correct"] += 1
            _set_text("#practice-result", "Correct!")
        else:
            _set_text("#practice-result", f"Not quite. Correct answer: {correct}")

        state["current_index"] = state["practice_queue"].pop() if state["practice_queue"] else None
        refresh_practice_view()

    @when("click", "#practice-reset")
    def on_practice_reset(event):
        _start_practice()
        _set_text("#practice-result", "")
        refresh_practice_view()

    _render_deck_selector()
    _set_active_deck(deck_name)
