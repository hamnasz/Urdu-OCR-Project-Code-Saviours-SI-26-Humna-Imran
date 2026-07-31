# Urdu OCR — A Fine-Tuned TrOCR Model for Extracting Text from Urdu Images

## The Problem

Optical character recognition for Urdu is harder than for Latin-script languages: Urdu
is written in the Nastaliq script, which is cursive, right-to-left, and highly
context-dependent — the shape of a letter changes depending on its position in a word.
Most off-the-shelf OCR tools are tuned for Latin or Naskh-style Arabic text and perform
poorly on Nastaliq. A model that reliably reads Urdu text from images has real
applications: digitizing scanned Urdu newspapers and books, reading text from signboards
for accessibility tools, or making handwritten/printed Urdu documents searchable.

## How It Works

This project fine-tunes [TrOCR](https://huggingface.co/microsoft/trocr-base-printed), a
transformer model built from two parts: a vision encoder that reads the pixels of an
image, and a text decoder that turns what it "sees" into characters. The base model
was pretrained on printed English text, so it already understands the general task of
"turn image into text" — fine-tuning adapts that ability to Urdu specifically, using a
custom dataset of Urdu text images paired with their correct transcriptions (see
Dataset Details below). During fine-tuning, the model is shown each image alongside its
correct Urdu label and gradually adjusts its internal weights to reduce the gap between
its predictions and the correct answer.

## Live Demo

**[Try it here](https://YOUR-APP-NAME.streamlit.app)** ← replace with your deployed Streamlit URL

## How to Run It Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR-USERNAME/Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran.git
cd Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week5

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`. Upload an image with Urdu text to test it.

## Dataset Details

- **Size:** ~[FILL IN — total rows in labels.csv, e.g. 200+] labeled images
- **Sources:** synthetic images generated with the Noto Nastaliq Urdu and Noto Naskh
  Arabic fonts over text pulled from an Urdu news corpus, plus manually collected
  images from newspapers, books, and signboards
- **Variety:** multiple fonts, font sizes, and background styles to help the model
  generalize beyond a single visual style

## Results

- **Accuracy (exact match):** [FILL IN]% — from Step 3 of the Week 4 notebook
- **Character Error Rate (CER):** [FILL IN]
- **Word Error Rate (WER):** [FILL IN]
- **Training loss:** went from [FILL IN] to [FILL IN] over [FILL IN] epochs

> Pull these numbers from `week4_metrics.json` (saved alongside your model in Week 4)
> or from the printed output of the evaluation cell.

If accuracy is on the lower side: the dataset is still fairly small for the visual
complexity of Nastaliq script, and more training data — especially handwritten and
varied real-world samples rather than synthetic ones — would likely help most. Longer
training and hyperparameter tuning (learning rate, batch size) were also not
exhaustively explored given the project timeline.

## Credit

**[Your Full Name]**
Built during the Code Saviours ML/AI Internship — Batch SI-26.
