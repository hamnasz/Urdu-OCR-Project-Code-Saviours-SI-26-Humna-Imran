# Setup & Installation

This guide walks you through setting up the development environment to run the Urdu OCR project.

## Prerequisites

- **OS**: Ubuntu/Debian Linux (or Windows/macOS with similar tools)
- **Python**: 3.7 or later
- **Git**: For cloning the repository
- **pip**: Python package manager

## System-Level Setup

### Step 1: Install System Dependencies

**On Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install -y \
  python3 \
  python3-pip \
  python3-venv \
  tesseract-ocr \
  libtesseract-dev \
  git
```

**On macOS (using Homebrew):**

```bash
brew install python3 tesseract
```

**On Windows:**
- Download and install Python 3 from [python.org](https://python.org)
- Download and install Tesseract from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)
- Ensure both are added to your PATH

### Step 2: Verify Tesseract Installation

```bash
tesseract --version
```

You should see version information. If not, ensure Tesseract is in your PATH.

## Python Environment Setup

### Step 3: Clone the Repository

```bash
git clone https://github.com/Code-Saviours/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran.git
cd Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran
```

### Step 4: Create Virtual Environment

Creating a virtual environment isolates project dependencies from your system Python:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

**On Linux/macOS:**
```bash
source .venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

You should see `(.venv)` at the start of your terminal prompt.

### Step 5: Install Python Dependencies

Upgrade pip first:

```bash
pip install --upgrade pip
```

Install required packages:

```bash
pip install \
  jupyter \
  notebook \
  ipywidgets \
  numpy \
  pillow \
  matplotlib \
  opencv-python \
  pytesseract \
  gdown
```

Or install from a requirements file (if one exists in the repo):

```bash
pip install -r requirements.txt
```

### Package Descriptions

| Package | Purpose |
|---------|---------|
| `jupyter`, `notebook` | Interactive Jupyter notebooks |
| `ipywidgets` | Interactive widgets in notebooks |
| `numpy` | Numerical computing |
| `pillow` | Image processing (PIL) |
| `matplotlib` | Data visualization |
| `opencv-python` | Advanced image processing (`cv2`) |
| `pytesseract` | Python wrapper for Tesseract OCR |
| `gdown` | Download files from Google Drive |

## Verification

### Test the Setup

1. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```
   This opens Jupyter in your browser (usually `http://localhost:8888`)

2. **Open a notebook:**
   - Navigate to `SI26-Week1/SI26_Week1_humna.ipynb`
   - Run a cell to verify imports work

3. **Test Tesseract:**
   In a notebook cell or Python script:
   ```python
   import pytesseract
   from PIL import Image
   
   # Test Tesseract
   print(pytesseract.get_tesseract_version())
   ```

4. **Test OpenCV:**
   In a notebook cell:
   ```python
   import cv2
   print(f"OpenCV version: {cv2.__version__}")
   ```

If all imports succeed without errors, your environment is set up correctly.

## Troubleshooting

### `pytesseract.TesseractNotFoundError`

**Problem:** Tesseract is not in your PATH.

**Solution:**
- Verify Tesseract installation: `tesseract --version`
- If not found, reinstall Tesseract and ensure it's added to PATH
- On Windows, after installing Tesseract, you may need to specify the path in Python:
  ```python
  import pytesseract
  pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
  ```

### `ModuleNotFoundError: No module named 'cv2'`

**Problem:** OpenCV not installed.

**Solution:**
```bash
pip install opencv-python
```

### `ModuleNotFoundError: No module named 'jupyter'`

**Problem:** Jupyter not installed.

**Solution:**
```bash
pip install jupyter notebook
```

### Virtual Environment Issues

**Problem:** Packages installed but not found when running Python.

**Solution:** Ensure you've activated the virtual environment:
```bash
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate.bat  # Windows (cmd)
# or
.venv\Scripts\Activate.ps1  # Windows (PowerShell)
```

## Running the Notebooks

After setup is complete:

1. **Activate the virtual environment** (if not already active)
2. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```
3. **Navigate to and open a notebook:**
   - `SI26-Week1/SI26_Week1_humna.ipynb` — Data exploration and font rendering
   - `SI26-Week2/SI26-Week2-Humna.ipynb` — Image processing and Tesseract experiments
4. **Run cells sequentially** — Follow the notebook flow from top to bottom

## Advanced: Using Conda

If you prefer Conda over venv:

```bash
conda create -n urdu-ocr python=3.9
conda activate urdu-ocr
conda install jupyter numpy pillow matplotlib opencv pytesseract
```

Then install system Tesseract separately (as above).

## Next Steps

- [Explore the Project Structure](Project-Structure.md)
- [Read the Technical Details](Technical-Details.md)
- [View Results & Gap Analysis](Results-Gap-Analysis.md)

---

**Need help?** See [FAQ](FAQ.md) for common issues.
