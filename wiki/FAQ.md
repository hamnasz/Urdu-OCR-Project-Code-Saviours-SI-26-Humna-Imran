# FAQ — Frequently Asked Questions

Quick answers to common questions about the Urdu OCR project.

## General Questions

### Q: What is this project about?

**A:** This project develops **Optical Character Recognition (OCR) for Urdu text written in Nastaliq script**. It's part of the Code Saviours SI-26 challenge led by Humna Imran. The work includes data collection, preprocessing pipelines, and gap analysis using Tesseract OCR as a baseline.

See [Project Overview](Project-Overview.md) for details.

---

### Q: Why is Urdu OCR important?

**A:** 

1. **Digital Preservation** — Digitize historical Urdu documents, books, and newspapers for archival
2. **Accessibility** — Make Urdu text searchable and accessible to digital systems
3. **Automation** — Extract Urdu text from forms, ID cards, bills for automated data entry
4. **Research Gap** — Existing OCR tools perform poorly on Nastaliq script; custom solutions are needed
5. **Minority Language Support** — Improve technology for underrepresented languages

---

### Q: How is this different from English OCR?

**A:**

| Aspect | English | Urdu (Nastaliq) |
|--------|---------|-----------------|
| **Script Type** | Latin, rectilinear | Cursive, diagonal |
| **Letter Joining** | Minimal | Extensive |
| **Position-Dependent Shapes** | No | Yes (start/middle/end/isolated) |
| **Training Data** | Abundant | Limited |
| **Existing Tools** | Excellent (Tesseract, etc.) | Poor (basic OCR only) |
| **Model Complexity** | Simpler | More complex |

See [Project Overview](Project-Overview.md) for more context.

---

## Technical Questions

### Q: What is Nastaliq script?

**A:** **Nastaliq** is a classical style of Urdu handwriting, highly cursive and decorative. Key characteristics:

- Text flows diagonally (top-right to bottom-left)
- Letters extensively joined with complex ligatures
- Letter shapes change based on position in word
- Common in handwritten Urdu, classical texts, poetry

Compare: **Naskh** (modern printed style, more rectilinear) vs. **Nastaliq** (classical, cursive)

---

### Q: What is OCR preprocessing?

**A:** **Preprocessing** prepares raw images for OCR by:

1. **Grayscale Conversion** — Remove color, keep intensity
2. **Denoising** — Remove scanning artifacts and dust
3. **Thresholding** — Convert to pure black/white (binary)
4. **Resizing** — Scale to manageable size while preserving aspect ratio

See [Technical Details](Technical-Details.md) for the full pipeline.

---

### Q: Why does Tesseract fail on Urdu?

**A:** Tesseract fails because:

1. **Training Data Mismatch** — Trained on Latin/Naskh, not Nastaliq
2. **Ligature Complexity** — Doesn't understand joined Nastaliq letterforms
3. **Layout Assumptions** — Assumes left-to-right single-line text, not right-to-left multi-line
4. **Hallucinations** — Invents characters when uncertain

**Results:** ~60-70% error rate on dense Urdu text

See [Results & Gap Analysis](Results-Gap-Analysis.md) for evidence.

---

### Q: What does "Character Error Rate (CER)" mean?

**A:**

$$\text{CER} = \frac{\text{Substitutions} + \text{Deletions} + \text{Insertions}}{\text{Total Ground Truth Characters}} \times 100\%$$

**Example:**
- Expected: "رضا" (3 characters)
- Got: "رظا" (1 substitution)
- CER = 1/3 ≈ **33%**

Lower CER is better. Target: <5% for production use.

---

## Setup & Installation

### Q: How do I set up the project?

**A:** Follow [Setup & Installation](Setup-Installation.md):

1. Clone repository
2. Install system dependencies (Python, Tesseract)
3. Create virtual environment
4. Install Python packages
5. Verify with test imports

Takes ~30 minutes.

---

### Q: Do I need Tesseract installed?

**A:** **Yes**, if you want to run the OCR experiments.

- **Linux/Mac:** `apt install tesseract-ocr` or `brew install tesseract`
- **Windows:** Download from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

`pytesseract` (Python package) is just a wrapper; Tesseract binary must be installed separately.

---

### Q: Can I run this on Windows?

**A:** **Yes**, but requires extra steps:

1. Install Python 3 from python.org
2. Install Tesseract from GitHub releases
3. Add Tesseract to PATH or configure in Python:
   ```python
   import pytesseract
   pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

See [Setup & Installation](Setup-Installation.md) for details.

---

### Q: What if I get `ModuleNotFoundError`?

**A:** You likely didn't activate your virtual environment:

```bash
source .venv/bin/activate   # Linux/Mac
# or
.venv\Scripts\activate.bat  # Windows
```

Then reinstall packages:
```bash
pip install jupyter opencv-python pytesseract
```

---

## Data & Dataset

### Q: How much data does the project have?

**A:** Currently **153 labeled images** from:
- Books (~50)
- Newspapers (~50)
- Synthetic (~20)
- Other (~33)

**Not enough for production model.** Recommendation: Expand to 5,000-50,000 images.

See [Data Management](Data-Management.md).

---

### Q: What format is the labels?

**A:** CSV file (`labels.csv`) with:

```csv
image_path,urdu_text,script_type
raw/books/book_001.png,"تاریخ بھارت",printed
raw/synthetic/synthetic_001.png,"ہمارا ملک",synthetic
```

Columns: image path, ground truth Urdu text, source type.

See [Data Management](Data-Management.md) for details.

---

### Q: Can I add more images to the dataset?

**A:** **Yes**, follow this process:

1. Collect image(s)
2. Preprocess if needed (crop, rotate, enhance)
3. Transcribe Urdu text manually
4. Add entry to `labels.csv`
5. Save image to appropriate `data/raw/` subdirectory
6. Commit and push

See [Data Management](Data-Management.md) for step-by-step guide.

---

## Models & Performance

### Q: Is there a trained model I can use?

**A:** **No**, this project hasn't trained a custom model yet. Currently only:
- ✅ Dataset collection (153 images)
- ✅ Preprocessing pipeline
- ✅ Tesseract baseline evaluation

**Next:** Build custom CNN or CNN+LSTM model.

---

### Q: What model architecture is recommended?

**A:**

| Model | Pros | Cons | Recommended For |
|-------|------|------|-----------------|
| **CNN** | Fast, simple | Limited accuracy | Proof-of-concept |
| **CNN+LSTM** | Good accuracy, variable-length | More complex | Production (80-90% accuracy) |
| **Transformer** | State-of-the-art | Needs 50k+ images | Future (95%+ accuracy) |

See [Technical Details](Technical-Details.md) for architecture details.

---

### Q: How long does training take?

**A:** Depends on model and hardware:

| Model | Dataset Size | GPU Time | CPU Time |
|-------|--------------|----------|----------|
| Simple CNN | 5k images | 30 min | 4 hours |
| CNN+LSTM | 20k images | 2 hours | 24 hours |
| Transformer | 100k images | 8 hours | Days |

---

## Contributing & Collaboration

### Q: Can I contribute to this project?

**A:** Contributions welcome! Areas:

- 📊 **Data Collection** — Add more labeled images
- 🔧 **Preprocessing** — Improve preprocessing pipeline
- 🤖 **Modeling** — Implement and train custom models
- 📚 **Documentation** — Improve wiki and comments
- 🧪 **Testing** — Test on new images, report issues

See [Project Structure](Project-Structure.md) to understand codebase.

---

### Q: How do I report issues?

**A:** 

1. Check [FAQ](FAQ.md) first (this page)
2. Open GitHub issue with:
   - **Title:** Clear problem description
   - **Steps to Reproduce:** How to see the issue
   - **Expected Behavior:** What should happen
   - **Actual Behavior:** What actually happened
   - **Environment:** OS, Python version, installed packages

---

### Q: Can I fork and extend this?

**A:** **Yes!** This project welcomes forks and extensions.

**Recommended extensions:**
- Add character-level bounding box annotations
- Implement CNN model
- Integrate other OCR engines (PaddleOCR, EasyOCR)
- Extend to other Urdu script styles (Naskh, Khat-e-Nasq)
- Multi-language support (add Persian, Arabic)

---

## Files & Notebooks

### Q: What's in SI26_Week1_humna.ipynb?

**A:** Week 1 exploratory notebook with:
- Data loading and exploration
- Image statistics (count, size, format)
- Nastaliq font rendering examples
- Label file creation
- Utility functions

See [Project Structure](Project-Structure.md).

---

### Q: What's in SI26-Week2-Humna.ipynb?

**A:** Week 2 processing and evaluation notebook with:
- Preprocessing pipeline code
- Image binarization examples
- Tesseract OCR experiments (5 test images)
- Error analysis and visualization
- Gap findings and recommendations

See [Project Structure](Project-Structure.md).

---

### Q: How do I run a notebook cell?

**A:**

1. Start Jupyter: `jupyter notebook`
2. Open notebook (e.g., `SI26-Week1/SI26_Week1_humna.ipynb`)
3. Click cell to select
4. Press `Shift + Enter` to run
5. Wait for output

Or use the **Run** button in Jupyter UI.

---

### Q: What if a notebook cell fails?

**A:** Check:

1. **Dependencies installed?** `pip install jupyter opencv-python pytesseract`
2. **Virtual environment activated?** `source .venv/bin/activate`
3. **Tesseract installed?** `tesseract --version`
4. **File paths correct?** Check path in cell
5. **Data exists?** Verify `data/raw/` has images

See [Setup & Installation](Setup-Installation.md) for troubleshooting.

---

## Licensing & Citation

### Q: What license is this project under?

**A:** Currently **no explicit license**. 

**Recommendation:** Repository owner should add one:
- **MIT** — For academic/open-source use
- **CC-BY-4.0** — For dataset + code combined
- **Apache 2.0** — For commercial-friendly open-source

---

### Q: How do I cite this project?

**A:** **Suggested citation:**

```
Imran, H. (2024). Urdu OCR: Nastaliq Script Recognition.
Code Saviours SI-26. Repository: [GitHub link]
```

**Bibtex:**
```bibtex
@software{imran2024urdu,
  title={Urdu OCR: Nastaliq Script Recognition},
  author={Imran, Humna},
  year={2024},
  publisher={Code Saviours SI-26},
  url={[GitHub link]}
}
```

---

## Performance & Evaluation

### Q: What are current OCR performance metrics?

**A:** From Week 2 Tesseract baseline:

- **Short Words:** ~70-80% accuracy
- **Complex Words:** ~10-30% accuracy
- **Multi-line Text:** ~5-20% accuracy
- **Overall CER:** ~60-70%

**Gap:** Need custom model for 80%+ accuracy.

See [Results & Gap Analysis](Results-Gap-Analysis.md).

---

### Q: How is accuracy measured?

**A:** Two metrics:

1. **Character Error Rate (CER):** Char-level accuracy (more strict)
2. **Word Error Rate (WER):** Word-level accuracy (less strict)

See [Technical Details](Technical-Details.md) for formulas.

---

## Troubleshooting

### Q: My Jupyter notebook won't start

**A:**

```bash
# Check if Jupyter installed
pip show jupyter

# Try reinstalling
pip install --upgrade jupyter notebook

# Try running on specific port
jupyter notebook --port 8889
```

---

### Q: Images look wrong after preprocessing

**A:** Check preprocessing steps:

1. **Grayscale conversion working?** Image should be gray, not color
2. **Thresholding working?** Image should be pure black/white
3. **Resize correct?** Check aspect ratio preserved

Add visualization code to debug:
```python
import matplotlib.pyplot as plt

plt.subplot(1,3,1); plt.imshow(original, cmap='gray'); plt.title('Original')
plt.subplot(1,3,2); plt.imshow(denoised, cmap='gray'); plt.title('Denoised')
plt.subplot(1,3,3); plt.imshow(binary, cmap='gray'); plt.title('Binary')
plt.show()
```

---

### Q: Tesseract not found error

**A:**

```bash
# Verify installation
tesseract --version

# If not found, reinstall
# Linux
sudo apt install tesseract-ocr

# Mac
brew install tesseract

# Windows: Download from GitHub
```

---

## Contact & Support

### Q: Who is the author?

**A:** **Humna Imran** — Lead for Code Saviours SI-26 Urdu OCR project

---

### Q: Where can I find more information?

**A:** Explore the wiki:
- [Home](Home.md) — Overview
- [Project Overview](Project-Overview.md) — Context & goals
- [Setup & Installation](Setup-Installation.md) — Getting started
- [Technical Details](Technical-Details.md) — Deep dive
- [Results & Gap Analysis](Results-Gap-Analysis.md) — Findings

---

**Not finding your question? Open an issue on GitHub!**
