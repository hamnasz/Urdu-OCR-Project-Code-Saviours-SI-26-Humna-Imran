# Project Overview

## What is OCR?

**Optical Character Recognition (OCR)** is the process of converting images of text—such as scanned pages, photographs, or screenshots—into machine-readable text that can be edited, searched, and processed by software. Instead of reading the image manually, an OCR system learns to interpret visual patterns and outputs the corresponding characters or words.

**Real-world applications of OCR:**
- Digitizing printed books and historical documents
- Extracting text from forms, ID cards, and official documents
- Automated data entry from bills and receipts
- Making searchable archives of old newspapers
- Accessibility tools for converting images to text

## Why Urdu OCR?

### Challenge: Nastaliq Script

Urdu is traditionally written in the **Nastaliq script**, which presents several challenges for OCR:

1. **Highly Cursive** — Letters are extensively joined and flow together
2. **Diagonal Flow** — Text flows diagonally rather than sitting on a straight baseline
3. **Position-Dependent Shapes** — Individual letters change form depending on position (start, middle, end, isolated)
4. **Complex Ligatures** — Multiple letters combine into special joined forms
5. **Limited Data** — Far less labeled Urdu OCR training data exists compared to English or Latin scripts

### Why This Project Matters

1. **Digitizing Historical Content** — Preserve and make searchable old Urdu books, government records, and newspapers
2. **Automated Data Entry** — Extract Urdu text from forms and official documents for digital systems
3. **Research Gap** — Existing OCR tools (like Tesseract) perform poorly on Nastaliq; custom solutions are needed
4. **Cultural Significance** — Supporting OCR for minority languages improves digital accessibility

## Project Goals

### Primary Objectives

- ✅ **Build a Dataset** — Collect 150+ labeled Urdu text images
- ✅ **Establish Baseline** — Measure Tesseract performance on Urdu
- 🔄 **Preprocess Images** — Develop a robust pipeline to convert raw images to OCR-ready formats
- 🎯 **Identify Gaps** — Document where existing tools fail and why
- 🤖 **Develop Custom Model** — Train a deep learning model specifically for Nastaliq OCR

### Success Metrics

- **Dataset Quality** — Diverse sources (books, newspapers, synthetic), accurately labeled
- **Preprocessing Robustness** — Handles single-line crops, full pages, and mixed layouts
- **Baseline Understanding** — Clear metrics showing where Tesseract succeeds/fails
- **Model Performance** — Custom model outperforms Tesseract on Nastaliq text

## Key Findings (Week 1 & 2)

### Week 1: Data Exploration

- Collected 153 raw images from:
  - 📚 Books (handwritten and printed Urdu)
  - 📰 Newspapers (printed Urdu with varying quality)
  - 🤖 Synthetic (generated using Nastaliq font)
  - 📄 Other (mixed sources)
- Created `labels.csv` with ground-truth text for all images
- Studied Nastaliq font rendering and characteristics

### Week 2: Gap Analysis

**Tesseract Baseline Results:**

Tesseract OCR (with Urdu language pack) was tested on 5 preprocessed images:

| Finding | Evidence |
|---------|----------|
| **Short words work** | Common words like "رضا", "ایک", "کا" recognized correctly |
| **Long/complex words fail** | Words with heavy ligatures like "قاضی", "انتخاب" mangled or dropped |
| **Hallucinations** | Invented characters (digits, symbols) not in source |
| **Layout sensitivity** | Single-line crops: better accuracy; full pages: major failures |
| **Spacing matters** | Loanwords with letter-spacing (e.g., "ڈونٹ وری") better recognized |

**Conclusion:** Tesseract's accuracy collapses on dense, multi-ligature Nastaliq script—which is most real Urdu text. A custom model trained specifically for Nastaliq is necessary.

## Repository Structure

```
├── SI26-Week1/                          # Week 1 work: Data exploration
│   ├── SI26_Week1_humna.ipynb          # Exploratory notebook
│   ├── data/
│   │   ├── raw/                         # 153 raw images
│   │   │   ├── books/
│   │   │   ├── newspaper/
│   │   │   ├── synthetic/
│   │   │   └── other/
│   │   └── labels.csv                   # Ground truth text
│   ├── NotoNastaliqUrdu-Regular.ttf     # Nastaliq font
│   └── Other/
│
├── SI26-Week2/                          # Week 2 work: Image processing & gap analysis
│   ├── SI26-Week2-Humna.ipynb          # Preprocessing & OCR experiments
│   ├── README_gap_analysis_section.md  # Detailed gap analysis
│   └── data/
│       └── processed/                   # Preprocessed images
│
└── wiki/                                 # This wiki
```

## Team & Attribution

- **Author & Lead**: Humna Imran
- **Challenge**: Code Saviours SI-26
- **Institution/Organization**: Code Saviours

## Next Steps

1. **Refine Preprocessing** — Continue optimizing the image binarization pipeline
2. **Expand Dataset** — Collect more labeled images for robust training
3. **Baseline Comparison** — Test other OCR tools (PaddleOCR, EasyOCR)
4. **Model Architecture** — Design CNN/Transformer architecture for Nastaliq
5. **Training** — Train custom model on collected dataset
6. **Evaluation** — Benchmark against Tesseract and other baselines

---

**For more details**, explore the wiki pages or check the Jupyter notebooks in the repository.
