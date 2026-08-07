# SI26-Week4 — Unified Urdu OCR Pipeline: Data Expansion, Fine-Tuning & Audit

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/blob/main/SI26-Week4/SI26_Week4_humna.ipynb)

Part of the [Urdu OCR Project — Code Saviours SI-26](https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran) internship series (Humna Imran). This week's notebook is the core modeling deliverable: it merges the dataset-expansion work with TrOCR fine-tuning and a full code audit into a single, three-phase pipeline.

## Contents

| File | Description |
|---|---|
| `SI26_Week4_humna.ipynb` | Single Colab notebook — 69 cells (~37 code, ~32 markdown), the only file currently in this folder |

Earlier in its history this folder also held several parallel notebook variants (`_OPTIMIZED`, `_codespace`, `_jupyterlab`, `_LOCAL_RTX3060`, and a stray Week‑5 file) that were later merged or deleted — see [Version History](#version-history) below.

## Overview

The notebook fine-tunes [`microsoft/trocr-base-printed`](https://huggingface.co/microsoft/trocr-base-printed) (a vision-encoder / RoBERTa-decoder `VisionEncoderDecoderModel`) to read Urdu **Nastaliq** script, and is organized into three phases:

### Phase 1 — Data Pipeline & Preprocessing
- **1.1 Synthetic rendering** — text rendered to line images via Pillow's raqm/HarfBuzz shaping (`direction="rtl", language="ur"`), across multiple fonts, with rotation/blur/gaussian-noise/background augmentation.
- **1.2 PDF extraction** — text-layer PDFs cropped per line and paired with extracted text via `pypdfium2` + `pdfplumber`.
- **1.3 DOCX extraction** — paragraph text pulled from user-supplied `.docx` files and pushed through the same synthetic renderer.
- **1.8 Public datasets** — pulls in **UTRSet-Real** (~11k rows) and **UTRSet-Synth** (~20k rows), both CC BY-NC-4.0, to make up for the small (263-row) original corpus; `UPTI` is wired in but off by default, and IIITH is excluded since its authors mark it test-only.
- **1.4 Merge** — all sources merged into one `labels.csv` (`image, text, category` schema), with automatic backup before each merge.
- **1.5–1.6** — loads `TrOCRProcessor`, and empirically measures `MAX_LENGTH` from the real tokenizer instead of hardcoding it.
- **1.7** — validates every image path and caches preprocessed tensors, dropping unresolvable rows with a printed count instead of failing mid-training.

### Phase 2 — Fine-Tuning
- Checkpoint/resume support so a disconnected Colab session doesn't lose a training run, mixed precision, LR schedule + gradient clipping, and best-checkpoint selection by validation CER.
- Reports exact-match accuracy, **CER** (Character Error Rate), and **WER** (Word Error Rate).
- Auto-surfaces the worst predictions and a visual grid of sample predictions (green border = exact match, red = mismatch).
- Saves evaluation metrics/predictions to Google Drive so results survive a runtime disconnect.

### Phase 3 — Code Audit & Optimization
- **3.1** recaps the original run's failure (0% accuracy, every prediction decoding to `�`) and its two root causes.
- **3.2** profiles data-loading vs. compute time from Phase 2's training loop.
- **3.3** empirically probes the largest batch size the GPU can sustain.
- **3.4** sanity-checks the learning rate against a few candidate values.
- **3.5** confirms which epoch was actually selected as the best checkpoint.

The finished model is pushed to the **Hugging Face Hub** via `push_to_hub()` — that's what Week 5's Streamlit app loads at inference time.

## Requirements

Installed in-notebook via:
```
pip install transformers==4.57.6 "pillow<12" pandas sentencepiece protobuf jiwer matplotlib huggingface_hub pdfplumber pypdfium2 python-docx gdown
```
`torch`/`torchvision` are intentionally left at whatever Colab has preinstalled, to avoid a version mismatch. A GPU runtime is expected (batch-size probing and mixed precision are skipped/meaningless on CPU).

## Getting Started

1. Open the notebook in Colab (badge above) with a **GPU runtime** (Runtime → Change runtime type → GPU).
2. Run the **Setup** cell — it mounts Google Drive and clones the repo into `REPO_DIR` (persisted on Drive so checkpoints survive a runtime reset).
3. Add a `HF_TOKEN` secret in Colab (Hugging Face access token) so the notebook can log in to the Hub.
4. Run Phase 1 → Phase 2 → Phase 3 cells in order.
5. Before Step 5, fill in `HF_REPO_ID` (e.g. `your-hf-username/trocr-urdu-si26-unified`) so the trained model gets pushed somewhere Week 5 can load it from.
6. Save the notebook back to GitHub via **File → Save a copy in GitHub** (don't try to `git push` the data/model folders — they're large/binary and redundant with the Hub/repo already).

## Key Findings

The original Week 4 run scored **0% accuracy (0/22)**, with every test prediction decoding to the Unicode replacement character. Two compounding causes, both addressed in this notebook:
- A **path-convention bug** in `labels.csv` silently dropped 153 of 263 rows (58%) — fixed by `resolve_image_path()`'s fallback logic.
- `microsoft/trocr-base-printed`'s text decoder is RoBERTa, pretrained only on English — it had never seen Urdu script, which is the running theory (backed by others hitting the same wall on Urdu/Arabic/Persian TrOCR fine-tunes) for why so much training data/time is needed. Section 2.8 covers alternative checkpoints to consider if this architecture proves inadequate.

## Version History

The commit history under `SI26-Week4/` runs from **26 Jul 2026 to 6 Aug 2026** — 94 commits total, contributed under several different GitHub accounts (mostly Colab's "Save a copy in GitHub" autosave, which commits as whichever account is signed in). The notebook grew from **23 cells (12 code)** at the initial commit to **69 cells (~37 code)** in the current version.

### Major milestones

| Date | Commit | Change |
|---|---|---|
| 2026-07-26 | `bf1c39e` | **Initial commit** — Week 4 notebook added: TrOCR fine-tuning pipeline with evaluation metrics and visualizations. |
| 2026-07-31 | `df468a2` | Adapted to run natively in a Codespace instead of Colab (dropped the git-clone/Drive-mount steps, saved checkpoints/model to local disk). Surfaced the two root-cause bugs later fixed in Phase 1/2: 153/263 rows silently skipped from a labels.csv path mismatch, and every prediction decoding to a solid block of `�`. |
| 2026-07-31 | `c8d0ad8`…`b4811e2` | Follow-up fixes for that Codespace variant: added missing pandas/torch install & import cells, fixed a torch `ModuleNotFoundError`, corrected execution counts, added clearer training/eval output logging, handled a kernel-crash error. |
| 2026-08-01 | `98c28a8` | Additional notebook variants added to the folder. |
| 2026-08-02 | `9e75911`, `1eede8d`, `caf6586`, `cf5f9b1` | Cleanup — deleted the `_OPTIMIZED`, stray Week‑5 dataset-expansion, `_jupyterlab`, and `_codespace` notebook variants as the project converged on one canonical file. |
| 2026-08-02 | `a4ee2be` → `6b5a8d3` | A `.env` file was briefly committed, then removed the same day. |
| 2026-08-02 | `17d54ea` | **"Renamed"** — merged the separate `SI26_Week4_humna_LOCAL_RTX3060.ipynb` variant back into `SI26_Week4_humna.ipynb` (~2,700 lines net removed by consolidating the two files into one). |
| 2026-08-02 | `478ff0d` | Install cell updated to force the kernel's own Python interpreter for `pip install`, so packages land in the right environment. |
| 2026-08-02 | `71450d9` | Corpus-loading cell made resilient — falls back to `headlines.csv.tar.gz` if the plain CSV is missing, raises a clear error if neither file exists. |
| 2026-08-02 | `730ba6c` | A `FileNotFoundError` hit while loading `SI26-Week3/corpus/headlines.csv` got captured (the bug the following commit fixes). |
| 2026-08-02 | `a48e126` | Rendering helper updated to detect a missing `libraqm` install and fall back to plain Pillow text layout instead of crashing on RTL Urdu shaping. |
| 2026-08-03 | `0485978` | Added `drive.mount("/content/drive")`; `REPO_DIR` moved onto Google Drive so the cloned repo and training checkpoints persist across Colab runtime resets instead of being lost every session. |
| 2026-08-02 – 08-06 | ~60 commits | Incremental "Created using Colab" / "Add files via upload" checkpoint saves as the notebook was iterated on cell-by-cell, committed under several contributing accounts (Developer Hamna, hamnaology, Git Girliee, Gitiee Flower, comicsz, Nikkiw, Github Girliee, bubbletics, developerhooria-cell, rihotutu). |
| 2026-08-05 | `2108635` | **"Fixed"** — bug-fix pass. |
| 2026-08-06 | `9c5dae2` | Notebook re-uploaded ("Add files via upload"). |
| 2026-08-06 | `d14e5a2` | Latest commit on `main` at time of writing. |

## Known Limitations / Notes

- The original 263-row hand-collected corpus is too small to fine-tune a 334M-parameter sequence model on its own — Section 1.8's public dataset pull-in exists specifically to address that.
- `microsoft/trocr-base-printed`'s decoder was never pretrained on Urdu; expect a long training runway before predictions stop looking like noise.
- Batch-size probing and the profiling report are only meaningful on an actual GPU runtime — both effectively no-op on CPU.
- Don't push the cloned data/checkpoint folders back to GitHub — they're large/binary; the trained model belongs on the Hugging Face Hub via `push_to_hub()`.

## Author

**Humna Imran** — Code Saviours ML/AI Internship, Batch SI-26
Repository: [hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran](https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran)
