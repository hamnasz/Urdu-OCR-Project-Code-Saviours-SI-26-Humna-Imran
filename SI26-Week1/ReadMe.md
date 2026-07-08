# Urdu OCR Project | Code Saviours SI-26 | Humna Imran

## Week 1 — Research Summary

**What is OCR (Optical Character Recognition)?**

OCR is the process of converting text from images such as scanned pages, photos, or screenshots into machine-readable text that can be edited, searched, and processed by software. Instead of reading the image manually, an OCR system learns to interpret visual patterns and output the corresponding characters or words. In practice, OCR is used to digitize printed and handwritten content so it can be stored and analyzed more easily.

**Why is Urdu OCR harder than English OCR?**

Urdu OCR is more difficult because Urdu is normally written in the Nastaliq script, which is highly cursive and flows diagonally rather than sitting neatly on a straight baseline like Latin text. Individual letters change shape depending on whether they appear at the start, middle, end, or in isolation of a word, which increases the number of visual forms the model must learn. In addition, there is far less publicly available labeled Urdu OCR training data than there is for English, making it harder to build accurate systems.

**What are 2 real-world situations where Urdu OCR would be useful?**

One important use case is digitizing historical Urdu documents, government records, and old newspapers so they can be preserved and searched easily. Another practical application is reading Urdu text from forms, ID cards, utility bills, or official documents so that data can be entered automatically into digital systems.

## Week 1 — Data Collection Progress

- [x] 50+ images from existing datasets (Source 1)
- [x] 30+ real photos/screenshots (Source 2)
- [x] 20+ synthetic generated images (Source 3)
- [x] `data/labels.csv` complete with ground-truth text for all images

## Project Structure

```
data/
├── raw/
│   ├── newspaper/
│   ├── books/
│   ├── synthetic/
│   └── other/
└── labels.csv
```

## Notes

The repository currently contains 153 raw images across books, newspapers, synthetic samples, and other Urdu text sources, along with a label file that provides ground-truth text for the collected samples.
