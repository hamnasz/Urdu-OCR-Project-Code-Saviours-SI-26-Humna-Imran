# Urdu OCR Project | Code Saviours SI-26 | [Your Full Name]

## Week 1 — Research Summary

**What is OCR (Optical Character Recognition)?**

[Write your own 3+ sentence answer here. Core idea to include: OCR converts
text in an image -- a scan, photo, or screenshot -- into machine-readable,
editable text, by having a model "read" pixels and output the
characters/words it recognizes.]

**Why is Urdu OCR harder than English OCR?**

[Write your own 3+ sentence answer here. Core ideas to include: Urdu is
typically written in Nastaliq script, which is cursive/diagonal rather than
sitting on a flat horizontal baseline like Latin script, making character
segmentation harder. Urdu letters also change shape depending on position
in a word (isolated/initial/medial/final forms), multiplying the number of
visual forms a model has to learn. There's also far less publicly available
labeled Urdu OCR data compared to English.]

**What are 2 real-world situations where Urdu OCR would be useful?**

[Write your own 3+ sentence answer here. Examples to draw from: digitizing
historical/government Urdu documents and old newspapers so they become
searchable and preserved; reading Urdu text from ID cards (CNIC), utility
bills, or forms to auto-fill data in apps -- a common real need in
Pakistan.]

## Week 1 — Data Collection Progress

- [ ] 50+ images from existing datasets (Source 1)
- [ ] 30+ real photos/screenshots (Source 2)
- [ ] 20+ synthetic generated images (Source 3)
- [ ] `data/labels.csv` complete with ground-truth text for all images

## Project Structure

```
data/
├── raw/
│   ├── newspaper/
│   ├── books/
│   ├── signboards/
│   ├── synthetic/
│   └── other/
└── labels.csv
```
