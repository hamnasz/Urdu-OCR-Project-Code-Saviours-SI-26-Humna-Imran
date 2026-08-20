# Urdu OCR Project — Code Saviours SI-26

**Author:** Humna Imran
**Program:** Code Saviours ML/AI Internship, Batch SI-26
**Project:** Optical Character Recognition for Urdu (Nastaliq script) using a fine-tuned TrOCR transformer model
**Repository:** [hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran](https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://urdu-ocr-project-code-saviours-si-26-humna-imran.streamlit.app/)

**Live demo:** Try the deployed Streamlit app: https://urdu-ocr-project-code-saviours-si-26-humna-imran.streamlit.app/

---

## Overview

This repository documents a 5-week applied ML project: building an OCR system that reads Urdu text
out of images. It moves through the full pipeline a real OCR project needs — collecting and labeling
data, testing an off-the-shelf baseline, expanding and validating a training set, fine-tuning a
transformer model, debugging why the model wasn't learning, and shipping a small web app around the
result.

Urdu is normally written in **Nastaliq**, a cursive, right-to-left script where each letter's shape
changes depending on where it sits in a word (isolated, initial, medial, or final form), and where
text flows diagonally rather than sitting on a flat baseline. General-purpose OCR engines are mostly
trained on Naskh-style printed Arabic/Urdu or Latin script, and — as this project verifies directly in
Week 2 — perform poorly on Nastaliq as a result. That gap is the reason this project exists: to fine-tune
a model specifically on Nastaliq Urdu rather than relying on a general OCR engine.

## Table of Contents

- [Repository Structure](#repository-structure)
- [Week-by-Week Breakdown](#week-by-week-breakdown)
  - [Week 1 — Research & Initial Dataset](#week-1--research--initial-dataset-si26-week1)
  - [Week 2 — Preprocessing & Baseline OCR](#week-2--preprocessing--baseline-ocr-si26-week2)
  - [Week 3 — Dataset Expansion](#week-3--dataset-expansion-si26-week3)
  - [Week 4 — Fine-Tuning, Debugging & Audit](#week-4--fine-tuning-debugging--audit-si26-week4)
  - [Week 5 — Deployment](#week-5--deployment-si26-week5)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Dataset Details](#dataset-details)
- [Key Findings & Debugging History](#key-findings--debugging-history)
- [Current Status & Known Limitations](#current-status--known-limitations)
- [Licensing & Attribution](#licensing--attribution)
- [Contact](#contact)

---

## Repository Structure

```
Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/
├── README.md
├── Code Saviours (SMC-PRIVATE) Limited — Internship 3 Week Report.pdf
│
├── SI26-Week1/                          # Research + first labeled dataset
│   ├── SI26_Week1_humna.ipynb
│   ├── ReadMe.md                        # Week 1 research answers & progress checklist
│   ├── NotoNastaliqUrdu-Regular.ttf     # Font used for synthetic rendering
│   ├── data/
│   │   ├── labels.csv                   # image, text, category
│   │   └── raw/
│   │       ├── books/                   # 35 scanned book-page images
│   │       ├── newspaper/               # 38 scanned newspaper images
│   │       ├── other/                   # 60 UTRSet-derived line images
│   │       ├── synthetic/               # 20 font-rendered synthetic images
│   │       └── synthetic_v2/            # 110 font-rendered synthetic images
│   └── Other/
│       ├── book.zip / newspaper.zip / signboard.zip   # source scan archives
│       └── utrset_real_download/
│
├── SI26-Week2/                          # Preprocessing pipeline + Tesseract baseline
│   ├── SI26-Week2-Humna.ipynb
│   ├── README_gap_analysis_section.md   # Baseline results + gap analysis writeup
│   └── data/processed/                  # 153 binarised/preprocessed images
│
├── SI26-Week3/                          # Dataset expansion via UTRSet + synthetic corpus
│   ├── SI26_Week3_humna.ipynb
│   ├── corpus/
│   │   ├── headlines.csv                # ~137K Urdu news headlines (source corpus)
│   │   └── headlines.csv.tar.gz
│   └── fonts/
│       ├── NotoNastaliqUrdu.ttf
│       └── NotoNaskhArabic-Variable.ttf
│
├── SI26-Week4/                          # Unified data pipeline + TrOCR fine-tuning + audit
│   └── SI26_Week4_humna.ipynb
│
└── SI26-Week5/                          # Streamlit inference app
    ├── app.py
    ├── requirements.txt
    └── README.md
```

Each week's folder is largely self-contained (own notebook, own `data/` where relevant), and the
notebooks are meant to be read/run in numeric order — later weeks build directly on the datasets and
findings from earlier ones.

---

## Week-by-Week Breakdown

### Week 1 — Research & Initial Dataset (`SI26-Week1/`)

Lays the groundwork: what OCR is, why Urdu is a harder case than English/Latin OCR, and two real-world
use cases (digitizing historical Urdu newspapers/government records; auto-reading Urdu text from CNICs,
utility bills, and forms). Full written answers are in `SI26-Week1/ReadMe.md`.

On the data side, this week produced the project's first labeled dataset: **263 image–text pairs** in
`data/labels.csv`, combining:

| Source folder | Count | Description |
|---|---|---|
| `raw/books/` | 35 | Scanned book pages |
| `raw/newspaper/` | 38 | Scanned newspaper pages |
| `raw/other/` | 60 | Real printed Urdu lines from UTRSet-Real |
| `raw/synthetic/` | 20 | Synthetically rendered text (v1) |
| `raw/synthetic_v2/` | 110 | Synthetically rendered text (v2) |

Synthetic images are rendered using the **Noto Nastaliq Urdu** font (`NotoNastaliqUrdu-Regular.ttf`,
included in this folder) with proper RTL/Urdu shaping.

### Week 2 — Preprocessing & Baseline OCR (`SI26-Week2/`)

Builds an image preprocessing pipeline and runs **Tesseract OCR** (`urd` language pack) as a baseline,
to quantify exactly how much a general-purpose OCR engine struggles with Nastaliq before justifying a
custom model.

**Preprocessing pipeline** (grayscale → resize → denoise → binarize) went through three iterations,
documented in `README_gap_analysis_section.md`:

1. **Fixed threshold + hard resize** — `cv2.threshold(img, 127, 255, THRESH_BINARY)` with every image
   forced into `(512, 128)`. Uneven lighting on real photos produced speckled "dotted" noise, and the
   hard resize stretched/warped Urdu's joined-up letterforms.
2. **Otsu's method + aspect-preserving resize with padding** — fixed the dotted-noise problem, but
   running Otsu binarization *after* pasting onto a white-padded canvas skewed the histogram so badly
   that entire images were classified as solid black.
3. **Binarize before padding, no fixed canvas** — Otsu now runs only on the real image content before
   padding; the fixed `(800, 160)` canvas was also dropped in favor of a bounded resize (only
   scale down if too large / up if too small, aspect ratio always preserved), since a fixed wide/short
   canvas crushed tall, portrait full-page scans into unreadable slivers.

**Baseline results** — Tesseract was run on 5 representative images (short line crops and full pages):

| Image | Result |
|---|---|
| `utrset_050.png` | Best of the five; short common words survived, longer ligature-heavy words dropped |
| `utrset_046.png` | Near-total failure; only one recoverable fragment |
| `book_021.png` | Mostly unreadable; transliterated loanword recognizable; hallucinated characters (×, stray digits) with no source equivalent |
| `book_015.png` | Similarly garbled, more hallucinated characters |
| `newspaper_021.png` | Isolated heading text recognized correctly; dense body text and header badly garbled, plus a hallucinated number |

**Conclusion:** Tesseract's accuracy collapses once text moves past short, spaced-out words into dense,
multi-ligature Nastaliq script — the overwhelming majority of real Urdu text — and it periodically
hallucinates characters that don't exist in the source. This directly motivates fine-tuning a
Nastaliq-specific model rather than using an off-the-shelf OCR engine tuned for Naskh/Latin text.

### Week 3 — Dataset Expansion (`SI26-Week3/`)

Expands the training set using **UTRNet's UTRSet-Real and UTRSet-Synth** datasets (ICDAR'23, Rahman,
Ghosh & Arora — IIIT Delhi), which provide real scanned printed Urdu text lines (mapped to the
`newspaper`/`book` categories) and computer-generated Urdu text images (mapped to `synthetic`).
UTRSet is released under **CC BY-NC-SA 4.0** for academic/research use.

Also introduced:
- A ~137,000-row **Urdu news headline corpus** (`corpus/headlines.csv`) used as source text for
  synthetic line rendering.
- The **`NotoNaskhArabic-Variable`** font, alongside Nastaliq, to add font-style variety.
- A `torch.utils.data.Dataset` wrapper around `labels.csv` (skipping rows whose image file doesn't
  exist yet), a `TrOCRProcessor`-based train/test split, and `DataLoader`s previewed with a real batch
  — the direct input to Week 4's fine-tuning loop.

The notebook also flags that no small, verifiable public dataset exists for Urdu **signboards** or
**handwriting**; those categories rely on the project's own collected photos (and, as a stretch option,
contacting CLE Pakistan for a handwriting corpus).

### Week 4 — Fine-Tuning, Debugging & Audit (`SI26-Week4/`)

The core modeling notebook, structured in three phases:

**Phase 1 — Data Pipeline & Preprocessing**
- Synthetic rendering (multiple fonts + augmentation: rotation, blur, gaussian noise, varied paper-tone backgrounds)
- Text-layer PDF extraction (via `pypdfium2` + `pdfplumber`, for user-supplied PDFs with a real text layer)
- DOCX paragraph extraction
- A dedicated section (1.8) pulling in the public **UTRSet-Real** (~11,000 rows) and **UTRSet-Synth**
  (~20,000 rows) datasets, both CC BY-NC-4.0, with `UPTI` (CLE Lahore) wired in but off by default; the
  IIITH set is deliberately excluded since its creators designate it test-only.
- All sources merge into `labels.csv` under one `image, text, category` schema
- `MAX_LENGTH` is measured empirically from the real tokenizer rather than hardcoded, and every image
  path is validated and preprocessed tensors are cached once rather than recomputed every epoch

**Phase 2 — Fine-Tuning**
- Base checkpoint: [`microsoft/trocr-base-printed`](https://huggingface.co/microsoft/trocr-base-printed)
  (a `VisionEncoderDecoderModel`: vision-transformer encoder + RoBERTa text decoder)
- Checkpoint/resume support (so a disconnected Colab session doesn't lose a training run), mixed
  precision, LR schedule + gradient clipping, and best-checkpoint selection by validation CER (not just
  whichever epoch runs last)
- Reports exact-match accuracy plus **CER** (Character Error Rate) and **WER** (Word Error Rate)
- Auto-surfaces the worst-performing predictions and a visual grid of sample predictions

**Phase 3 — Code Audit & Optimization**
- Recaps the original run's failure mode, profiles data-loading vs. compute time, empirically probes
  the largest batch size the GPU can sustain, and sanity-checks the learning rate against a few
  candidate values

The final trained model is intended to be pushed to the **Hugging Face Hub** via `push_to_hub()`, which
is what Week 5's app loads from.

### Week 5 — Deployment (`SI26-Week5/`)

A minimal **Streamlit** app (`app.py`) for interactive inference:
- Upload a PNG/JPG containing Urdu text
- The app runs the fine-tuned TrOCR model (loaded from a Hugging Face Hub model repo, cached via
  `@st.cache_resource`) and displays the extracted text in a right-to-left, Urdu-styled text block
- Falls back to a clear error message if `MODEL_ID` isn't pointed at a valid, public model repo yet

Dependencies (`requirements.txt`): `streamlit`, `transformers==4.57.6`, `torch`, `pillow<12`,
`sentencepiece`, `protobuf`.

---

## Tech Stack

| Tool / Library | Role |
|---|---|
| **TrOCR** (`microsoft/trocr-base-printed`) | Fine-tuned vision-encoder/text-decoder OCR model |
| **Tesseract OCR** | Baseline comparison engine (Week 2) |
| **PyTorch** | Model training |
| **Hugging Face Transformers / Hub** | Model loading, fine-tuning, and hosting |
| **OpenCV** | Image preprocessing (grayscale, resize, denoise, Otsu binarization) |
| **Pillow (+ raqm/HarfBuzz)** | RTL-aware synthetic Urdu text rendering |
| **pdfplumber / pypdfium2** | Text-layer PDF line extraction |
| **python-docx** | DOCX paragraph extraction |
| **gdown** | Downloading UTRSet datasets from Google Drive |
| **jiwer** | CER / WER computation |
| **Streamlit** | Web app for interactive OCR demo |
| **Jupyter / Google Colab** | Experimentation and training environment |

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip or conda
- For Week 2's Tesseract baseline: `sudo apt install tesseract-ocr tesseract-ocr-urd libtesseract-dev` (Ubuntu/Debian; on GitHub Codespaces run `sudo apt-get update` first)
- A GPU is strongly recommended for Week 4's fine-tuning notebook (it is designed to run on Google Colab)

### Installation

```bash
git clone https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran.git
cd Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install jupyter notebook ipywidgets numpy pillow matplotlib opencv-python pytesseract \
            pandas torch transformers datasets evaluate jiwer sentencepiece protobuf \
            pdfplumber pypdfium2 python-docx gdown
```

### Running the Notebooks

Open and run in order:
1. `SI26-Week1/SI26_Week1_humna.ipynb`
2. `SI26-Week2/SI26-Week2-Humna.ipynb`
3. `SI26-Week3/SI26_Week3_humna.ipynb`
4. `SI26-Week4/SI26_Week4_humna.ipynb` (recommended on Google Colab with a GPU runtime; there's a
   built-in "Open in Colab" badge at the top of the notebook)

### Running the Demo App (Week 5)

```bash
cd SI26-Week5
pip install -r requirements.txt
streamlit run app.py
```

Before running, set `MODEL_ID` at the top of `app.py` to the Hugging Face Hub repo the fine-tuned
model was pushed to in Week 4 (e.g. `hamnaheh/urdu-ocr-si26`). The app opens at
`http://localhost:8501`.

---

## Dataset Details

- **Base labeled set (Week 1):** 263 image–text pairs across books, newspapers, UTRSet-derived lines,
  and two rounds of synthetic rendering.
- **Preprocessed set (Week 2):** 153 binarized/cleaned images used for the Tesseract baseline test.
- **Expanded set (Week 4, Phase 1):** grows the base set by folding in UTRSet-Real (~11K) and
  UTRSet-Synth (~20K) samples (capped per source during development), plus any user-supplied PDFs/DOCX
  and additional synthetic renders — one committed training run loaded **3,280** samples
  (2,296 train / 492 validation / 492 test).
- **Text source for synthetic rendering:** a ~137,000-row Urdu news headline corpus
  (`SI26-Week3/corpus/headlines.csv`).
- **Fonts:** Noto Nastaliq Urdu (primary) and Noto Naskh Arabic (secondary, for style variety), both
  SIL Open Font License.
- **Schema:** every source normalizes to the same `image, text, category` columns in `labels.csv`.

---

## Key Findings & Debugging History

This project's Week 4 notebook documents an unusually transparent debugging trail, worth summarizing
for anyone reading the code:

1. **Original run: 0% accuracy, every prediction decoded to `�`.** Root-caused to two compounding bugs:
   - A **path-convention mismatch** in `labels.csv` silently dropped 153 of the original 263 rows (58%)
     from training — fixed by adding fallback path resolution that checks both conventions the file had
     accumulated.
   - A 334M-parameter model was only getting **~66 total gradient steps** (88 examples × 3 epochs ÷
     batch size 4) — nowhere near enough for a decoder that has never seen Urdu script to learn a new
     vocabulary from scratch.
2. **Architecture caveat:** `microsoft/trocr-base-printed`'s text decoder is **RoBERTa, pretrained only
   on English**. The vision encoder transfers across scripts reasonably well, but the decoder has to
   learn Urdu essentially from zero during fine-tuning — which is why this project needs many more
   epochs than a similarly-sized English fine-tuning task would, and why the notebook explicitly flags
   accuracy as having "a real ceiling worth watching honestly." Community-fine-tuned alternatives
   (e.g. `cxfajar197/urdu-ocr`) and a decoder-swap approach used by others fine-tuning TrOCR on
   Arabic-script languages are noted as follow-up options, not yet adopted here.
3. **After fixing the two bugs above,** a 20-epoch run brought validation CER down from 2.51 to **1.365**
   with steadily falling training loss (~17 → ~1.5–1.8) — real learning — but exact-match accuracy
   stayed at 0% because predictions were dominated by runaway repeated character sequences (e.g.
   `"ررررررررر"`), a classic **exposure bias** symptom: teacher-forced training loss doesn't penalize
   the free-running repetition that shows up at inference time.
4. **Mitigations applied:** `repetition_penalty` / `no_repeat_ngram_size` on generation, an explicit
   `eos_token_id`, epochs raised from 20 to 40, and a fix making synthetic-image generation idempotent
   (90 of 180 `synthetic_v2` rows had no matching image file on Drive).
5. **A later audit** on the next run found validation CER fluctuating (0.952 → 1.212 → 1.078) across
   early epochs while training loss fell steadily and steeply — confirmed as the *same* exposure-bias
   pattern still partially visible early in training, not a new overfitting problem, since overfitting
   requires loss to stay flat/low while validation error rises, which isn't what happened here. A
   character-level error breakdown (insertions/deletions/substitutions) and a loss-vs-CER diagnostic
   dashboard were added so this distinction can be read directly instead of eyeballed.

---

## Current Status & Known Limitations

- The committed `SI26-Week4` notebook's training cell output is from a **run in progress** (visible up
  to roughly batch 210 of 287 in an epoch) — the final accuracy/CER/WER numbers for the current
  40-epoch run, the loss chart, and the pushed Hugging Face model repo are not yet baked into this
  README, since they hadn't finished computing as of the last commit reflected here. Check the notebook's
  own output cells (Phase 2, sections 2.3–2.7) and `week4_metrics.json` for up-to-date numbers before
  citing a specific accuracy figure.
- **`SI26-Week5/app.py` and `SI26-Week5/README.md` still contain placeholder values** (`MODEL_ID`,
  the deployed Streamlit URL, and the results table) that need to be filled in once a final model is
  pushed to the Hugging Face Hub.
- The **English-only RoBERTa decoder** in the base TrOCR checkpoint is a real, acknowledged ceiling on
  achievable accuracy — not merely a hyperparameter issue — and is the leading candidate for the next
  architecture change if results plateau.
- Dataset size, even after Week 4's expansion (~3,280 samples in one run), is still small for a
  334M-parameter sequence model and for the visual complexity of Nastaliq script; more real (not just
  synthetic) handwritten and varied-condition samples would likely help most.
- No public dataset exists for Urdu **signboards** or **handwriting** at the scale this project would
  need, so those categories depend on manually collected photos.
- No open-source license file is currently included in the repository (see below).

---

## Licensing & Attribution

- **This repository's own code/notebooks:** no explicit license file is currently included. This is
  coursework for the Code Saviours ML/AI Internship (Batch SI-26) and is not currently open for
  external contributions; if you'd like to use, extend, or reference this work, please contact the
  author.
- **UTRSet-Real / UTRSet-Synth** (used in Weeks 3–4): CC BY-NC-SA 4.0 / CC BY-NC-4.0 — academic and
  research use only. See the [UTRNet project repository](https://github.com/abdur75648/UTRNet-High-Resolution-Urdu-Text-Recognition#datasets) for citation details.
- **UPTI** (CLE Lahore, wired in but off by default in Week 4): research use per the source paper's terms.
- **Noto Nastaliq Urdu / Noto Naskh Arabic** fonts: SIL Open Font License.
- **`microsoft/trocr-base-printed`**: Hugging Face Hub model, MIT license.

---

## Contact

**Author:** Humna Imran
**Repository:** https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran

For questions or feedback, please open an issue in this repository.

---

*This README reflects the repository's committed state as of August 2026. Update the Results and
Current Status sections once the Week 4 training run and Week 5 deployment placeholders are finalized.*
