## Week 2 — Preprocessing & Baseline OCR Gap Analysis

### Preprocessing

All 153 raw images collected in Week 1 (35 books, 38 newspaper, 20 synthetic, 60 UTRSet/other)
were converted to grayscale, resized to a standard 512×128, denoised, and binarised. Processed
images are saved in `data/processed/`.

### Why We Need a Better Model

Five images — one from each source type — were tested with baseline Tesseract OCR (`lang='urd'`)
against the real ground-truth text from `data/labels.csv`.

| Image | Ground truth | Tesseract output | What went wrong |
|---|---|---|---|
| `books/book_001.png` | دیباچہ | *(empty)* | Portrait page (510×706) squashed into the fixed 512×128 canvas, destroying the text entirely |
| `newspaper/newspaper_001.png` | پہلی بات | *(empty)* | Same aspect-ratio distortion as above (466×705 → 512×128) |
| `synthetic/urdu_1.png` | پاکستان زندہ باد | پالسحا نے 2عدہ یاھ | Closer aspect ratio survived resizing, but output is gibberish — wrong/merged letters, a hallucinated digit |
| `other/utrset_000.png` | اندراج و تحریر شرعاً صرف مستحب اور پسندیدہ ہے وہ واجب نہیں کہ کسی شرعی | ا ام سپ لا | Almost all 13 words lost; only 4 meaningless fragments returned |
| `other/utrset_005.png` | مقدمات سے نجات مل سکتی ہے، نکاح کے ثبوت اورک دین مہر کے تعین میں سہولت ہوتی | ااع للا 2 کے | Nearly total word loss again, plus a hallucinated digit |

**Tesseract fails on Urdu because** the script it's actually tuned for is Naskh-style printed
Arabic, not the Nastaliq calligraphic style that almost all real Urdu text — books, newspapers,
and the UTRSet samples alike — is set in. Nastaliq is diagonal and cursive: letters slope
downward across the line instead of sitting on a flat baseline, each letter changes shape
depending on whether it's isolated or in the initial, medial, or final position within a word,
and neighbouring letters overlap and stack vertically rather than staying cleanly separated.
Tesseract's segmentation logic assumes clean, mostly-horizontal word boundaries, so on dense
Nastaliq lines it either merges separate letters into meaningless blobs or splits single letters
into multiple "characters" — exactly the fragment-soup seen in the UTRSet examples above. On top
of that, our own preprocessing pipeline made things measurably worse for the portrait-oriented
book and newspaper pages: forcing every image into a fixed 512×128 canvas regardless of its
original aspect ratio squashed tall pages so severely that no readable structure survived at all.
Between the script mismatch and the aspect-ratio distortion, it's clear a dedicated Urdu OCR
model — one trained specifically on Nastaliq letterforms, paired with preprocessing that
preserves each image's natural proportions — is genuinely necessary.
