# Urdu OCR Project — Code Saviours SI-26

**Author:** Humna Imran  
**Project:** Urdu Optical Character Recognition (OCR) using fine-tuned TrOCR model

## Overview

This repository contains a complete 5-week OCR project for recognizing text in Urdu (Nastaliq script). The project progresses from data exploration and font rendering through image preprocessing, and culminates in a fine-tuned TrOCR transformer model for extracting text from Urdu images.

Urdu OCR is challenging due to the complexity of Nastaliq script — a cursive, right-to-left script where character shapes depend on their position in words. This project demonstrates how transfer learning with vision transformers can be effectively applied to this problem.

## Repository Structure

### **SI26-Week1/** — Data Exploration & Font Rendering
- `SI26_Week1_humna.ipynb` — Initial data exploration, font rendering examples, and utility code
- `NotoNastaliqUrdu-Regular.ttf` — Nastaliq font for synthetic text rendering
- `data/` — Sample images and ground truth files

**Focus:** Understanding the Urdu text problem, setting up fonts, and exploring data sources.

### **SI26-Week2/** — Image Processing & OCR Baseline
- `SI26-Week2-Humna.ipynb` — Image preprocessing experiments and baseline OCR runs
- `README_gap_analysis_section.md` — Gap analysis and findings for Week 2
- `data/` — Dataset assets for experiments

**Focus:** Exploring traditional OCR approaches (Tesseract), identifying gaps in standard tools for Urdu, and analyzing what a fine-tuned model could improve.

### **SI26-Week3/** — Dataset Preparation & Augmentation
- Dataset curation and labeling pipeline
- Image augmentation strategies for robustness
- Creation of training/validation/test splits

**Focus:** Building a high-quality, diverse dataset for model training.

### **SI26-Week4/** — Model Training & Evaluation
- Fine-tuning the TrOCR base model on Urdu text images
- Training logs, metrics, and performance analysis
- Model checkpoints and evaluation results

**Focus:** Training the transformer model and measuring performance (accuracy, CER, WER).

### **SI26-Week5/** — Deployment & Live Demo
- `app.py` — Streamlit web app for interactive OCR inference
- `requirements.txt` — Python dependencies
- `README.md` — Deployment and usage instructions
- Trained model artifacts

**Focus:** Building a user-friendly interface and deploying the model.

## Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- For local Tesseract (Week 2): `sudo apt install tesseract-ocr` (Ubuntu/Debian)

### Installation

```bash
# Clone the repository
git clone https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran.git
cd Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install jupyter notebook ipywidgets numpy pillow matplotlib opencv-python pytesseract pandas torch transformers datasets evaluate
```

### Running the Notebooks

```bash
# Start Jupyter
jupyter notebook

# Open and run notebooks in order:
# 1. SI26-Week1/SI26_Week1_humna.ipynb
# 2. SI26-Week2/SI26-Week2-Humna.ipynb
# 3. SI26-Week3/ notebooks (dataset prep)
# 4. SI26-Week4/ notebooks (training & evaluation)
```

### Running the Live Demo (Week 5)

```bash
cd SI26-Week5
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. Upload an image containing Urdu text to test the model.

## Key Technologies & Tools

| Tool/Library | Purpose |
|---|---|
| **TrOCR** | Transformer-based OCR model (fine-tuned) |
| **Tesseract** | Baseline OCR for comparison (Week 2) |
| **PyTorch** | Deep learning framework |
| **Hugging Face Transformers** | Model fine-tuning and inference |
| **OpenCV** | Image preprocessing and augmentation |
| **Streamlit** | Web app for interactive demos |
| **Jupyter** | Experiment notebooks and exploration |

## Dataset

- **Composition:** Synthetic images (generated from Noto Nastaliq Urdu fonts) + real-world images (scanned newspapers, books, signboards)
- **Variety:** Multiple fonts, sizes, backgrounds, and scripts (Nastaliq + Naskh Arabic)
- **Labels:** Paired image-text transcriptions
- **Use:** Training, validation, and test sets prepared in Week 3

## Results Summary

Detailed metrics and results are in the **SI26-Week4** folder:
- **Model Accuracy:** [See Week 4 evaluation notebook]
- **Character Error Rate (CER):** [See Week 4 evaluation notebook]
- **Word Error Rate (WER):** [See Week 4 evaluation notebook]

The fine-tuned model outperforms baseline Tesseract on Urdu text (Nastaliq) due to its ability to learn script-specific patterns through transfer learning.

## File Organization Tips

- Each week's folder is self-contained with its own `data/` subdirectory
- Notebooks are numbered sequentially; run them in order
- Large model files are typically stored outside the repo or downloaded on-demand (see Week 4 & 5 notebooks)
- Refer to individual week README files for detailed documentation

## Troubleshooting

**Issue: Notebook can't find data files**
- Ensure you're running Jupyter from the project root directory
- Check that `data/` folders exist in each week's directory

**Issue: Tesseract errors (Week 2)**
- Install system package: `sudo apt install tesseract-ocr libtesseract-dev`

**Issue: Model download fails**
- Some notebooks download models from Hugging Face. Check your internet connection and disk space.

## Contribution & License

This repository contains coursework for the Code Saviours ML/AI Internship (Batch SI-26). It is not currently open for external contributions.

If you wish to use, extend, or reference this work, please contact the author.

No explicit license file is included. If you are the repository owner and want to add one, consider MIT, Apache-2.0, or another appropriate open-source license.

## Contact

**Author:** Humna Imran  
**Repository:** https://github.com/hamnasz/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran

For questions or feedback, please open an issue in this repository.

---

**Last Updated:** August 2026  
**Project Status:** Completed (5-week internship project)
