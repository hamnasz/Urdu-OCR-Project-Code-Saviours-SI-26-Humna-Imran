# Urdu OCR Project — SI-26 (Humna Imran)

## Overview

This repository contains coursework and experiments for Optical Character Recognition (OCR) on Urdu (Nastaliq script) performed as part of SI-26 by Humna Imran. It includes Jupyter notebooks, example datasets, and assets (including a Nastaliq font) used to develop, analyze, and prototype OCR workflows.

## Repository structure

- `SI26-Week1/`
  - `SI26_Week1_humna.ipynb` — Notebook containing initial data exploration, font rendering examples, and utility code.
  - `NotoNastaliqUrdu-Regular.ttf` — Included Nastaliq font used for synthetic rendering.
  - `data/` — Data assets used in Week 1 (sample images, ground truth, etc.).
  - `Other/` — Miscellaneous files used during Week 1.
- `SI26-Week2/`
  - `SI26-Week2-Humna.ipynb` — Notebook with image processing experiments, OCR runs, and gap-analysis notes.
  - `data/` — Data assets used in Week 2.
  - `README_gap_analysis_section.md` — Gap analysis and notes for Week 2.

## Key files

- `SI26-Week1/SI26_Week1_humna.ipynb` — Exploratory notebook.
- `SI26-Week2/SI26-Week2-Humna.ipynb` — Image processing and OCR experiments.

## Dependencies

The notebooks primarily use standard Python data and imaging libraries. Recommended environment (Ubuntu / Debian):

System packages (Ubuntu/Debian):

```
sudo apt update
sudo apt install -y python3 python3-pip python3-venv tesseract-ocr libtesseract-dev
```

Python packages (install into a virtual environment):

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install jupyter notebook ipywidgets numpy pillow matplotlib opencv-python pytesseract gdown
```

Notes:
- `pytesseract` is a Python wrapper around the Tesseract OCR engine — ensure `tesseract-ocr` is installed on the system.
- `opencv-python` provides `cv2` used for image pre-processing.

## Usage

1. Clone the repository and open a terminal inside the project folder.
2. Prepare a Python virtual environment and install dependencies (see above).
3. Start Jupyter:

```
jupyter notebook
```

4. Open and run the notebooks:
   - `SI26-Week1/SI26_Week1_humna.ipynb` — run cells to reproduce data preparation and font rendering samples.
   - `SI26-Week2/SI26-Week2-Humna.ipynb` — run the image processing and OCR experiment cells. The notebook includes example usages of `pytesseract` and `cv2`.

## Data and assets

- The `data/` folders inside `SI26-Week1` and `SI26-Week2` contain example images and files used by the notebooks. Inspect these folders before running the notebooks — some cells expect files to be present or will download them automatically (via `gdown` or other utilities).
- The included font `NotoNastaliqUrdu-Regular.ttf` can be used for synthetic image generation and rendering Urdu text in the notebooks.

## Reproducing experiments

- Follow the Usage steps to run the notebooks interactively.
- Many cells contain comments and small helper utilities; run cells sequentially. If a cell downloads data (e.g., via `gdown`), allow it to complete before continuing.

## Contribution

This repository contains coursework and is not currently set up for external contributions. If you want to collaborate or extend the experiments, please open an issue or contact the author.

## License

The repository does not include an explicit license file. If you are the repository owner and want to add a license, consider adding a `LICENSE` file (e.g., MIT, Apache-2.0) describing reuse terms.

## Contact

Repository owner and author: Humna Imran (see repository metadata for contact links).
