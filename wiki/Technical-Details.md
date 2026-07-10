# Technical Details

This page covers the technical aspects of the Urdu OCR project, including preprocessing pipeline, OCR methodology, and model considerations.

## Understanding OCR Pipeline

```
Raw Image
    ↓
[Grayscale Conversion]
    ↓
[Denoising]
    ↓
[Adaptive Thresholding (Otsu)]
    ↓
[Aspect-Preserving Resize]
    ↓
[Binary Image Output]
    ↓
[OCR Engine or Model]
    ↓
[Recognized Text]
```

## Preprocessing Pipeline

### 1. Grayscale Conversion

**Purpose:** Reduce color channels to single intensity channel

**Method:** `cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`

**Why:** Most OCR engines and neural networks work better with grayscale images. Color channels add noise without useful information for text recognition.

### 2. Noise Removal (Denoising)

**Purpose:** Remove scanning artifacts, dust, and compression noise

**Methods:**
- **Morphological Operations:** Erode + Dilate (remove small noise)
- **Gaussian Blur:** Smooth the image before thresholding
- **Bilateral Filtering:** Preserve edges while denoising

**Why:** Raw scanned images contain speckles, dust particles, and ink variation that confuse OCR.

### 3. Adaptive Thresholding (Otsu's Method)

**Purpose:** Convert grayscale image to pure binary (black/white)

**Algorithm:** `cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)`

**How it works:**
- Calculates optimal threshold value to separate foreground (text) from background
- Unlike fixed threshold (e.g., pixel > 127 → white), adapts to each image
- Minimizes intra-class variance between black and white regions

**Why Otsu's method:**
- ✅ Handles varying lighting conditions (uneven shadows, glare)
- ✅ Works across different image types (books, newspapers, synthetic)
- ✅ No manual tuning of threshold value needed
- ❌ Can fail on very low-contrast images

**Evolution in Project:**

**Round 1 (Failed):** Fixed threshold + hard resize
- Problem: Uneven lighting → speckled noise from shadowed regions

**Round 2 (Partial Success):** Otsu after padding
- Problem: Padding (white canvas) skewed histogram → entire text turned black

**Round 3 (Success):** Otsu before padding, dynamic canvas sizing
- Solution: Apply Otsu to real content first, then pad already-binarized image
- Result: Works for both single-line crops and full-page scans

### 4. Aspect-Preserving Resize

**Purpose:** Scale images to manageable size while maintaining text proportions

**Key Principles:**
- Calculate aspect ratio: `ratio = width / height`
- Scale down if image exceeds max dimension (e.g., 2048px)
- Scale up if image is smaller than min dimension (e.g., 256px)
- Add padding only if needed; preserve aspect ratio

**Why aspect ratio matters:**
- Urdu text is highly cursive; squashing/stretching distorts character shapes
- Position-dependent letterforms (start/middle/end) become unrecognizable if stretched

**Fixed Canvas vs. Dynamic Canvas:**

❌ **Fixed Canvas (512×128):** Crushed tall pages into horizontal sliver

✅ **Dynamic Canvas:** Scale but preserve aspect ratio, no forced dimensions

### 5. Output: Binary Image

**Result:** Pure black-and-white image (pixel value = 0 or 255)

**Format:** PNG or grayscale NumPy array

**Ready for:**
- Tesseract OCR processing
- Custom neural network training
- Character segmentation algorithms

## Tesseract OCR

### What is Tesseract?

**Tesseract** is an open-source OCR engine developed by HP and maintained by Google. It uses:
- **Feature extraction** to identify character shapes
- **Pattern matching** against trained models
- **Markov Random Fields** to resolve ambiguous characters using context

### Tesseract for Urdu

**Language Pack:** `urd` (Urdu)

**Invocation:**
```python
import pytesseract
from PIL import Image

img = Image.open('processed_image.png')
text = pytesseract.image_to_string(img, lang='urd')
```

**Tesseract Configuration Options:**

```python
# Page Segmentation Mode (PSM)
pytesseract.image_to_string(img, config='--psm 6', lang='urd')
# PSM options:
# 0 = Orientation and script detection only
# 3 = Fully automatic (default)
# 6 = Single uniform block of text
# 7 = Single text line
```

### Known Limitations on Nastaliq

| Issue | Reason |
|-------|--------|
| **Short words work** | Common patterns well-trained in model |
| **Complex ligatures fail** | Model not trained on Nastaliq-style joining |
| **Hallucinations** | Trained on cleaner Naskh script; invents characters |
| **Full page collapse** | Assumes left-to-right Latin layout; breaks on RTL multi-line Urdu |
| **Mixed text/image failure** | Can't separate illustration backgrounds from text |

### Example Failure Modes

**Input:** "اپنی رضا مندی سے ایک قاضی کا انتخاب کریں"

**Expected Output:** اپنی رضا مندی سے ایک قاضی کا انتخاب کریں

**Actual Output:** ا رضا مد ات ایک توا ھی کا ا کرس دراس مواش گنی کیا

**Analysis:**
- Simple words ("ایک", "کا", "رضا") recognized
- Complex words ("قاضی", "انتخاب") mangled or dropped
- Character substitutions frequent (ج → ج + noise)

---

## Image Processing Code Example

### Complete Preprocessing Pipeline

```python
import cv2
import numpy as np

def preprocess_image(image_path, min_size=256, max_size=2048):
    """
    Preprocess image for OCR:
    1. Load and convert to grayscale
    2. Denoise
    3. Apply Otsu's thresholding
    4. Resize preserving aspect ratio
    5. Return binary image
    """
    
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Image not found: {image_path}")
    
    # Step 1: Denoise (bilateral filtering preserves edges)
    denoised = cv2.bilateralFilter(img, 9, 75, 75)
    
    # Step 2: Otsu's adaptive thresholding
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Step 3: Resize preserving aspect ratio
    height, width = binary.shape
    aspect_ratio = width / height
    
    # Scale if needed
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(new_height * aspect_ratio)
    elif width < min_size and height < min_size:
        if width < height:
            new_width = min_size
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min_size
            new_width = int(new_height * aspect_ratio)
    else:
        new_width, new_height = width, height
    
    # Resize using aspect ratio
    resized = cv2.resize(binary, (new_width, new_height), 
                        interpolation=cv2.INTER_LANCZOS4)
    
    return resized

# Usage
processed = preprocess_image('raw_image.png')
cv2.imwrite('processed_image.png', processed)
```

## Custom Model Considerations

### Architecture Options for Nastaliq OCR

#### 1. CNN (Convolutional Neural Network)

**Strengths:**
- Excellent at capturing local spatial features (character shapes)
- Efficient for character/word-level recognition

**Architecture Example:**
```
Input (grayscale image)
  ↓
[Conv2D → ReLU → MaxPool] × 3  (feature extraction)
  ↓
[Flatten]
  ↓
[Dense(256) → ReLU → Dropout]
  ↓
[Dense(num_characters)]  (output layer)
```

**Considerations:**
- Need many examples per character class
- Fixed input size may struggle with variable-length words

#### 2. RNN + CNN (Sequence-to-Sequence)

**Strengths:**
- Handles variable-length text sequences
- Can learn character context and ligature patterns
- Used by modern OCR systems (Tesseract4+, PaddleOCR)

**Architecture Example:**
```
Input (grayscale image line)
  ↓
[CNN: Extract features from image]
  ↓
[LSTM/GRU: Process feature sequence]
  ↓
[Output: Character probabilities]
```

**Considerations:**
- More complex; requires more training data
- Better generalization to unseen text patterns

#### 3. Vision Transformer (ViT)

**Strengths:**
- State-of-the-art performance on many vision tasks
- Captures global context better than CNNs

**Considerations:**
- Requires very large training dataset (100k+ images)
- Computationally expensive

### Data Requirements for Custom Model

| Model Complexity | Min. Training Images | Training Time | Accuracy |
|------------------|---------------------|---------------|----------|
| Simple CNN | 5k-10k | 1-2 hours | ~70-80% |
| CNN + RNN | 10k-50k | 2-8 hours | ~85-90% |
| Transformer | 50k-200k | 8-48 hours | ~90%+ |

**Current Dataset:** 153 images (insufficient for production model)

**Recommendation:** 
- Start with simple CNN for proof-of-concept
- Augment dataset with rotations, warping, synthetic generation
- Transition to CNN+LSTM as dataset grows

### Data Augmentation Strategies

```python
# Techniques to multiply dataset without collecting more images

1. **Rotation:** ±5° for natural variation in scanning angle
2. **Elastic Distortion:** Simulate paper wrinkles and curves
3. **Noise Addition:** Gaussian noise, salt-and-pepper noise
4. **Scaling:** Small random scaling to simulate different DPI
5. **Shear:** Simulate skewed scanning or text slant
6. **Synthetic Text:** Generate more images using Nastaliq font
```

---

## Performance Metrics

### Character Error Rate (CER)

$$\text{CER} = \frac{\text{Substitutions} + \text{Deletions} + \text{Insertions}}{\text{Total Characters in Ground Truth}} \times 100\%$$

**Example:**
- Expected: "رضا مندی" (7 characters)
- Got: "رضا ن دی" (with insertion) = 1 error
- CER = 1/7 ≈ 14%

### Word Error Rate (WER)

$$\text{WER} = \frac{\text{Wrong Words}}{\text{Total Words}} \times 100\%$$

### Confidence Score

Each OCR engine returns confidence for each character (0-100%)

```python
# Tesseract confidence per word
results = pytesseract.image_to_data(img, lang='urd', output_type=pytesseract.Output.DICT)
confidences = results['conf']  # per-word confidence scores
```

---

## References

- **Tesseract Documentation:** https://github.com/tesseract-ocr/tesseract
- **OpenCV Documentation:** https://docs.opencv.org/
- **Urdu Script:** https://en.wikipedia.org/wiki/Urdu_alphabet
- **Nastaliq Font:** https://fonts.google.com/specimen/Noto+Nastaliq+Urdu

---

**Next:** [View Results & Gap Analysis](Results-Gap-Analysis.md) to see Tesseract baseline performance.
