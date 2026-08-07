# SI26-Week5 — Urdu OCR Streamlit App

Deployment week for the [Urdu OCR Project — Code Saviours SI-26](https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran) internship series. This folder wraps the TrOCR model fine-tuned in `SI26-Week4/` in a small, single-page Streamlit app: upload an image with Urdu text, get the extracted text back, styled right-to-left.

**Author:** Humna Imran — Code Saviours ML/AI Internship, Batch SI-26

---

## Contents

| File | Purpose |
|---|---|
| `app.py` | The Streamlit app — model loading, image upload UI, inference, RTL result display |
| `requirements.txt` | Pinned/loose dependencies needed to run the app |
| `README.md` | This file |

There is no `data/` or model-weights folder here by design — the fine-tuned model lives on the Hugging Face Hub, not in this repo (see [Model Loading](#model-loading) below).

---

## What `app.py` Does

1. **Page setup** — configures a centered Streamlit page titled "Urdu OCR — Code Saviours SI-26" with a notepad emoji favicon.
2. **Model loading** (`load_model()`, wrapped in `@st.cache_resource` so it only runs once per session, not on every interaction):
   - Picks `cuda` if available, otherwise falls back to `cpu`.
   - Loads a `TrOCRProcessor` and a `VisionEncoderDecoderModel` from `MODEL_ID`.
   - Puts the model in `.eval()` mode (inference only, no gradient tracking).
   - If loading fails (e.g. `MODEL_ID` is still the placeholder, or the repo is private/missing), the app shows a specific error message pointing at `MODEL_ID` in `app.py` rather than crashing silently, and calls `st.stop()`.
3. **Upload + inference:**
   - Accepts a `.png`, `.jpg`, or `.jpeg` upload, converts it to RGB, and displays it back to the user.
   - Runs the image through the processor to get `pixel_values`, then `model.generate()` with `max_length=128` under `torch.no_grad()`.
   - Decodes the generated token IDs back to text with `processor.batch_decode(..., skip_special_tokens=True)`.
4. **Result display** — the extracted text is rendered in a bordered `<div>` with `dir="rtl"` and `lang="ur"`, at a larger font size, so Urdu displays correctly right-to-left instead of in the browser's default left-to-right block. If no text comes back, the user sees a warning instead of a blank box.
5. **Empty state** — before any upload, the app just shows an info prompt asking for an image.

---

## Model Loading

`app.py` currently points `MODEL_ID` at a placeholder:

```python
MODEL_ID = "your-hf-username/urdu-ocr-si26"  # <-- replace after pushing to the Hub
```

**This needs to be updated** once the Week 4 fine-tuning run finishes and the model is pushed to the Hub. Two options are documented inline in `app.py`:

- **Option A — Hugging Face Hub model repo (recommended).** Push the fine-tuned model and processor from the Week 4 notebook:
  ```python
  from huggingface_hub import HfApi
  api = HfApi()
  api.create_repo("your-username/urdu-ocr-si26", repo_type="model")
  model.push_to_hub("your-username/urdu-ocr-si26")
  processor.push_to_hub("your-username/urdu-ocr-si26")
  ```
  Then set `MODEL_ID` to that same repo id. This avoids committing a 1GB+ model file to GitHub and avoids Git LFS entirely — the reason this option was chosen over storing weights in-repo.
- **Option B — a path inside the repo.** Point `MODEL_ID` at a relative path (e.g. `SI26-Week1/data/model`) instead. This requires Git LFS for the weights, since a plain `git push` won't handle a file that large.

---

## Setup & Running Locally

```bash
# From the repo root
cd SI26-Week5

# Install dependencies
pip install -r requirements.txt

# Set MODEL_ID in app.py to a valid Hugging Face model repo first, then:
streamlit run app.py
```

The app opens at `http://localhost:8501`. Upload a PNG or JPG containing Urdu text to test it.

### Running in a GitHub Codespace

This folder was built with a Codespace deployment in mind:

```bash
cd SI26-Week5
pip install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Codespaces will prompt to forward port 8501 — open it (set visibility to "Public" if you want to share the link) to reach the app in a browser.

### Deploying to Streamlit Community Cloud

1. Push this repo to GitHub (already done).
2. On [share.streamlit.io](https://share.streamlit.io), create a new app pointing at:
   - Repository: `hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran`
   - Branch: `main`
   - Main file path: `SI26-Week5/app.py`
3. Make sure `MODEL_ID` in `app.py` is already updated and pushed before deploying, since the app will fail to load the model otherwise.
4. Once live, the deployed URL replaces the placeholder in this README's demo link below.

---

## Dependencies

From `requirements.txt`:

| Package | Role |
|---|---|
| `streamlit` | Web app framework |
| `transformers==4.57.6` | `TrOCRProcessor` / `VisionEncoderDecoderModel` (pinned for reproducibility) |
| `torch` | Model inference backend |
| `pillow<12` | Image loading/conversion (capped below v12 for compatibility) |
| `sentencepiece` | Tokenizer dependency for the TrOCR text decoder |
| `protobuf` | Required by `sentencepiece`/`transformers` model loading |

---

## Live Demo

**[Try it here](https://YOUR-APP-NAME.streamlit.app)** — placeholder until the app is deployed to Streamlit Community Cloud (or another host) with a finalized `MODEL_ID`. Replace this link once deployed.

---

## Current Status & Known Limitations

- `MODEL_ID` in `app.py` is still a placeholder — the Week 4 training run this app depends on hadn't finished/been pushed to the Hub as of the last commit reflected in this repo. The app will show a clear load error until this is set to a real, public model repo id.
- The results/metrics table has intentionally been left out of this README rather than filled with placeholder numbers — pull final accuracy, CER, and WER from `week4_metrics.json` (saved alongside the model in Week 4) or the printed output of the notebook's evaluation cell once training completes, and add them here.
- No GPU inference path is assumed for hosting — `load_model()` falls back to CPU automatically, which works for a demo but will be noticeably slower per prediction than the GPU used for training.
- This app does no image preprocessing (denoising, binarization, RTL-aware cropping) before handing the raw upload to the processor — Week 2's preprocessing pipeline is not currently wired into this deployment. Users uploading noisy photos rather than clean scans may see worse results than the model's evaluation metrics suggest.

---

## Licensing & Attribution

- Coursework for the Code Saviours ML/AI Internship (Batch SI-26); no separate license file for this folder — see the repository root README for overall licensing notes.
- Base model: [`microsoft/trocr-base-printed`](https://huggingface.co/microsoft/trocr-base-printed), MIT license.

## Contact

**Author:** Humna Imran
**Repository:** https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran

For questions or feedback, open an issue in the repository.
