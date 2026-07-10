# Data Management

This page explains how data is organized, collected, labeled, and managed throughout the project.

## Dataset Overview

### Current Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Images** | 153 |
| **Total Size** | ~50 MB (raw), ~10 MB (processed) |
| **Ground Truth Annotations** | ✅ Complete (labels.csv) |
| **Script Types** | Printed, handwritten, synthetic |
| **Date Range** | 2024-2025 |

### Data Sources

| Source | Count | Description | Image Quality |
|--------|-------|-------------|---------------|
| **Books** | ~50 | Scanned pages from Urdu books | Medium-High |
| **Newspapers** | ~50 | Printed newspaper pages | Medium |
| **Synthetic** | ~20 | Generated using Nastaliq font | High (clean) |
| **Other** | ~33 | Mixed: forms, documents, edge cases | Variable |
| **Total** | **153** | | |

---

## Data Directory Structure

### Raw Data Organization

```
SI26-Week1/data/raw/
├── books/
│   ├── book_001.png
│   ├── book_002.png
│   └── ... (~50 images)
├── newspaper/
│   ├── newspaper_001.png
│   ├── newspaper_002.png
│   └── ... (~50 images)
├── synthetic/
│   ├── synthetic_001.png
│   ├── synthetic_002.png
│   └── ... (~20 images)
├── other/
│   ├── utrset_001.png
│   ├── utrset_002.png
│   └── ... (~33 images)
└── README.txt (optional: data source documentation)
```

### Processed Data

```
SI26-Week2/data/processed/
├── book_001.png          # Same filename as raw, binarized
├── book_002.png
├── newspaper_001.png
├── synthetic_001.png
└── utrset_001.png
```

---

## Ground Truth Annotations

### labels.csv Format

**Location:** `SI26-Week1/data/labels.csv`

**Purpose:** Maps each image to its Urdu text content for training and evaluation

**CSV Columns:**

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `image_path` | String | `raw/books/book_001.png` | Path relative to data directory |
| `urdu_text` | String | `یہ اردو کا متن ہے` | Ground truth Urdu script |
| `script_type` | String | `printed` | Source classification |

### Example labels.csv

```csv
image_path,urdu_text,script_type
raw/books/book_001.png,"تاریخ بھارت ایک طویل اور رنگین کہانی ہے",printed
raw/books/book_002.png,"وہ اپنے گاؤں میں رہتے تھے",printed
raw/newspaper/newspaper_001.png,"صبح بخیر! آج کی خبریں",printed
raw/newspaper/newspaper_002.png,"کھیل کی دنیا سے تازہ ترین اپڈیٹ",printed
raw/synthetic/synthetic_001.png,"ہمارا ملک بہت خوبصورت ہے",synthetic
raw/other/utrset_001.png,"اردو ادب کا مقام بہت اہم ہے",handwritten
```

### Script Type Classifications

| Type | Description | Examples |
|------|-------------|----------|
| `printed` | Scanned or photographed printed Urdu text | Books, newspapers, official documents |
| `handwritten` | Handwritten Urdu script | Manuscripts, forms, personal notes |
| `synthetic` | Computer-generated using fonts | Generated images for training |
| `mixed` | Contains multiple types | Scanned forms with both printed + handwritten |

---

## Data Collection Pipeline

### Collection Steps

```
1. Source Identification
   ↓ (Books, newspapers, documents, public datasets)
   ↓
2. Image Acquisition
   ↓ (Scan, photograph, download, generate)
   ↓
3. Preprocessing (if needed)
   ↓ (Crop, correct orientation, enhance)
   ↓
4. Manual Annotation
   ↓ (Transcribe text in Urdu script)
   ↓
5. Quality Check
   ↓ (Verify text matches image)
   ↓
6. CSV Registration
   ↓ (Add to labels.csv)
   ↓
7. Archive
   ↓ (Store in data/raw/)
```

---

## Data Quality Assurance

### Validation Checklist

- [ ] Image is readable (not too blurry, rotated, or damaged)
- [ ] Urdu text is correctly transcribed
- [ ] Image filename matches entry in labels.csv
- [ ] No duplicate images in dataset
- [ ] Image format is supported (PNG, JPEG, BMP)
- [ ] Ground truth text uses correct Urdu Unicode characters

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Image too dark/faded | Poor scan quality | Re-scan at higher contrast or discard |
| Rotated 90° | Scanner orientation | Rotate with `cv2.rotate()` |
| Duplicate images | Collection oversight | Keep one, remove from CSV |
| Wrong Urdu transcription | Transcriber error | Re-verify against source |
| Missing diacritics | Unicode encoding | Add correct combining marks (Fatha, Damma, etc.) |

---

## Data Augmentation Strategy

### Synthetic Image Generation

Using the provided `NotoNastaliqUrdu-Regular.ttf` font:

```python
from PIL import Image, ImageDraw, ImageFont
import random

def generate_synthetic_image(urdu_text, font_size=48, rotation=0, noise=0):
    """Generate synthetic Urdu text image for augmentation"""
    
    # Create blank image
    img = Image.new('RGB', (1024, 256), color='white')
    draw = ImageDraw.Draw(img)
    
    # Load font
    font = ImageFont.truetype('NotoNastaliqUrdu-Regular.ttf', font_size)
    
    # Draw text
    draw.text((50, 50), urdu_text, fill='black', font=font)
    
    # Apply rotation
    if rotation != 0:
        img = img.rotate(rotation, fillcolor='white')
    
    # Add noise if specified
    if noise > 0:
        img = add_gaussian_noise(img, noise)
    
    return img

# Generate augmented dataset
for original_image in original_dataset:
    for angle in [-5, -2, 0, 2, 5]:  # Rotation angles
        for noise_level in [0, 1, 2]:  # Noise levels
            augmented = generate_synthetic_image(text, rotation=angle, noise=noise_level)
            augmented.save(f'augmented_{id}_{angle}_{noise_level}.png')
```

### Augmentation Techniques

| Technique | Parameter Range | Purpose |
|-----------|-----------------|---------|
| **Rotation** | ±5° | Simulate scanning angle variation |
| **Scaling** | 0.9-1.1× | Simulate different DPI/magnification |
| **Noise** | Gaussian (σ=0.5-2.0) | Simulate scan artifacts |
| **Elastic Distortion** | α=30-50 | Simulate paper wrinkles |
| **Shear** | ±0.1 rad | Simulate skewed text |
| **Elastic Distortion** | Varies | Simulate curved pages |

### Augmentation Impact

| Dataset Size | Strategy | Effective Training Size | Note |
|--------------|----------|------------------------|------|
| 153 original | None | 153 | Insufficient |
| 153 original | 10× augmentation | 1,530 | Better for CNN |
| 153 original | 100× augmentation | 15,300 | Good for CNN+LSTM |

---

## Data Splitting for Machine Learning

### Recommended Train/Validation/Test Split

**Raw Dataset (153 images):**
```
Training:   120 images (78%)   → For model training
Validation: 20 images (13%)   → For hyperparameter tuning
Test:       13 images (9%)    → For final evaluation
```

**Augmented Dataset (2,000+ images):**
```
Training:   1,500 images (75%)
Validation: 300 images (15%)
Test:       200 images (10%)
```

### Stratified Splitting

Ensure each split has representative distribution:

```python
from sklearn.model_selection import train_test_split

# Read labels
labels_df = pd.read_csv('labels.csv')

# Stratify by script_type (printed, handwritten, synthetic, etc.)
train, temp = train_test_split(labels_df, test_size=0.22, 
                               stratify=labels_df['script_type'])
val, test = train_test_split(temp, test_size=0.45,
                             stratify=temp['script_type'])
```

---

## Data Privacy & Attribution

### License & Reuse

- **Current Status:** No explicit license specified
- **Recommendation:** Add LICENSE file (e.g., CC-BY-4.0, MIT)
- **Attribution:** Always credit source images and authors

### Data Sources Citation

When dataset is expanded, include sources:

```
Books Collection:
  - Source: Urdu literature repository XYZ
  - License: CC-BY-SA 4.0
  - Date Accessed: 2024-XX-XX

Newspaper Collection:
  - Source: Historical newspaper archive ABC
  - License: Public domain
  - Date Accessed: 2024-XX-XX

Synthetic Data:
  - Generated using: NotoNastaliqUrdu font
  - Font License: Open Font License (OFL)
```

---

## Backup & Version Control

### Git Management

**Current:** `.gitignore` excludes large image files

```
# .gitignore example
SI26-Week1/data/raw/*.png
SI26-Week1/data/raw/**/*.png
SI26-Week2/data/processed/*.png
```

**Reason:** Image files stored locally; only tracked files are:
- CSV labels
- Code (notebooks, scripts)
- Documentation

### Backup Strategy

**Recommended:**
1. **Local Backup:** External drive copy of entire `data/` directory
2. **Cloud Backup:** Google Drive, AWS S3, or institutional storage
3. **Archive:** Zip dataset with metadata for long-term preservation

```bash
# Backup command
tar -czf urdu-ocr-dataset-backup-2024.tar.gz SI26-Week1/data/ SI26-Week2/data/
```

---

## Metadata Documentation

### Image Metadata Template

Create `data/MANIFEST.txt` documenting collection details:

```
URDU OCR DATASET MANIFEST
=========================

Collection Date: 2024-2025
Total Images: 153
Total Size: 50 MB (raw), 10 MB (processed)

SOURCES:
--------

Books (50 images):
  - Urdu literature collection, various publishers
  - Scanned at 300 DPI
  - Date Collected: 2024-Q1

Newspapers (50 images):
  - Historical Urdu newspapers, archive.org
  - Photographed from archives
  - Date Collected: 2024-Q2

Synthetic (20 images):
  - Generated using NotoNastaliqUrdu-Regular.ttf
  - Various text lengths and complexities
  - Date Generated: 2024-Q1

Other (33 images):
  - Mixed sources, edge cases
  - Includes forms, documents, test samples
  - Date Collected: 2024-Q1-Q3

QUALITY NOTES:
--------------
- All images manually verified for Urdu text accuracy
- Ground truth text in labels.csv
- Preprocessing pipeline applied to all images before use
```

---

## Data Growth Roadmap

### Phase 1: Foundation (Current)
- **Size:** 153 labeled images
- **Sources:** Books, newspapers, synthetic
- **Use:** Proof-of-concept, baseline testing

### Phase 2: Expansion
- **Size:** 5,000-10,000 labeled images
- **Sources:** Expanded collection + augmentation
- **Use:** Train simple CNN model

### Phase 3: Scale
- **Size:** 50,000+ labeled images
- **Sources:** Multiple languages/scripts, diverse formats
- **Use:** Train state-of-the-art model

### Phase 4: Production
- **Size:** 100,000+ labeled images
- **Sources:** Real-world documents, public datasets
- **Use:** Deployed OCR service

---

## Tools for Data Management

### Python Libraries

```python
import pandas as pd           # CSV/dataframe manipulation
import cv2                    # Image processing
import numpy as np            # Numerical operations
import matplotlib.pyplot as plt  # Visualization
from PIL import Image         # Image I/O
import json                   # Metadata storage
```

### Annotation Tools (for future use)

- **Roboflow:** Image dataset management and augmentation
- **LabelImg:** Bounding box annotation tool
- **CVAT:** Computer Vision Annotation Tool
- **Prodigy:** Interactive annotation tool

---

## Summary

**Data is the foundation of OCR model success.** This project maintains:

- ✅ 153 labeled images with ground truth text
- ✅ Organized directory structure by source type
- ✅ CSV-based annotation format for ML tools
- ✅ Preprocessing pipeline for consistent image quality
- ✅ Augmentation strategy to expand effective dataset size

**Next priority:** Expand to 5,000+ images and implement character-level bounding box annotations for robust model training.

---

**Related Pages:**
- [Technical Details](Technical-Details.md) — Image preprocessing methods
- [Project Structure](Project-Structure.md) — Directory organization
- [Setup & Installation](Setup-Installation.md) — Running notebooks with data
