## Why We Need a Better Model

We ran baseline [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (with the `urd` language pack)
on 5 preprocessed images from our dataset to establish a baseline and understand the gap our
custom model needs to close.

### Preview: Raw vs. Processed

A couple of examples of what our preprocessing pipeline actually does — original photographed/scanned
image on the left, cleaned-up binarised version (what Tesseract and our future model both see) on
the right. These are the same two image types discussed below: a short single-line crop and a full
page mixing text with an illustration.

**Line crop (utrset_050)**

| Raw | Processed |
|---|---|
| ![raw](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week1/data/raw/other/utrset_050.png) | ![processed](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week2/data/processed/utrset_050.png) |

**Line crop (utrset_046)**

| Raw | Processed |
|---|---|
| ![raw](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week1/data/raw/other/utrset_046.png) | ![processed](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week2/data/processed/utrset_046.png) |

**Full page with story text (book_021)**

| Raw | Processed |
|---|---|
| ![raw](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week1/data/raw/books/book_021.png) | ![processed](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week2/data/processed/book_021.png) |

**Full page with illustration (newspaper_021)**

| Raw | Processed |
|---|---|
| ![raw](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week1/data/raw/newspaper/newspaper_021.png) | ![processed](Urdu-OCR-Project-Code-Saviours-SI-26-Humna-Imran/SI26-Week2/data/processed/newspaper_021.png) |

> Note: these images live in `readme_images/` next to this README. If you move or rename this file,
> bring that folder along with it (or update the relative paths above) so the previews don't break
> on GitHub.

### Results

| Image | Actual Urdu Text | Tesseract Output | What Went Wrong |
|---|---|---|---|
| utrset_050.png | اپنی رضا مندی سے ایک قاضی کا انتخاب کریں اور اس قاضی کو تنفیذ کی طاقت اور | ا رضا مد ات ایک توا ھی کا ا کرس دراس مواش گنی کیا طاقت ور | Best result of the five. Short, common words like رضا، ایک، کا، طاقت came through fine, but anything longer or more ligature-heavy (قاضی، انتخاب، تنفیذ) got mangled or dropped entirely. |
| utrset_046.png | اور تحصیلوں میں قاضیوں اور نائب قاضیوں کا تقرر کرے تو تمام مشکلات کا حل ہوجانا | کھلوں یں یں زا وا غو ںان ررکر ےکم ملا ت اع ہەہاتا | Basically a total miss — only one weak fragment (ررکر, vaguely echoing تقرر) is recoverable. Same script, same font, same preprocessing as the line above it, yet way worse — shows how inconsistent Tesseract's failures are, not just how frequent. |
| book_021.png | Full page of dialogue-style story text (too dense/small in the source scan to hand-transcribe line-by-line) | Mostly unreadable, but the transliterated phrase "ڈونٹ وری" (don't worry) is recognizable | Loanwords written with more letter-spacing survived better than native joined-up Urdu script. Also threw in characters that don't exist anywhere in the source — a stray ×, Arabic-Indic digits, invisible RTL marks — pure hallucination, not misreading. |
| book_015.png | Not available — we don't have a raw/original copy of this page to compare against, only the processed version | Similarly garbled, with more invented characters (stray digits, symbols) that have no basis in real text | Same collapse pattern as book_021: dense multi-line Nastaliq paragraphs break down almost completely. Worth grabbing the raw original for this one so we can do a proper word-level comparison later. |
| newspaper_021.png | Page header, then the heading "جسامت" ("build/size"), then a body paragraph | Heading "جسامت" came through perfectly. Everything else (the header bar and the body paragraph) was garbled, plus a hallucinated "737" that isn't in the source at all | Big, isolated heading text is easy for Tesseract. Small dense body text competing with a dark background bar and no clear paragraph structure is where it falls apart. |

### Summary

> Tesseract fails on Urdu because its accuracy basically collapses once you move past short,
> isolated, or spaced-out words into dense, multi-ligature Nastaliq script — which is most of
> real Urdu text. Short common words and transliterated loanwords (less cursive joining) got
> through some of the time, but anything built from several joined letterforms was consistently
> dropped, truncated, or swapped for the wrong characters. It also just makes things up sometimes
> — stray digits, symbols, invisible control marks that don't exist anywhere in the original —
> which points to a model trained on cleaner Naskh-style printed text that doesn't generalize to
> Nastaliq's diagonal, stacked, position-dependent letterforms. Full pages with multiple lines
> and paragraphs failed even harder than single-line crops, likely because Tesseract's layout
> assumptions are built around left-to-right, Latin-style spacing, and break down further once
> you add right-to-left multi-line text and mixed text/illustration layouts. All of this backs up
> why this project needs a model trained specifically for Nastaliq Urdu instead of leaning on an
> off-the-shelf OCR engine.

### Preprocessing note

Getting to clean, OCR-ready images took a few rounds of trial and error, and each round taught us
something about what breaks Urdu text specifically.

**Round 1 — fixed threshold + hard resize.** Our first pass used a single fixed brightness cutoff
(`cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)`) and forced every image into the same `(512, 128)`
box regardless of its original shape. On real photographed pages with uneven lighting, one fixed
cutoff can't handle shadowed regions properly, so it turned into speckled "dotted" noise. The hard
resize also stretched or squashed characters, which is especially bad for Urdu's joined-up script.

**Round 2 — Otsu's method + aspect-preserving resize with padding.** We switched to Otsu's method
(`cv2.THRESH_OTSU`), which recalculates the best threshold per image instead of using one fixed
number, and to a resize that preserves aspect ratio and pads onto a fixed canvas instead of
warping the image. This fixed the dotted-noise problem — but it introduced a new one we didn't
catch until we tested with a wider range of images: running Otsu *after* pasting the resized image
onto a padded white canvas meant Otsu's threshold was calculated over the whole canvas, padding
included. Since the padding is a big block of pure white, it skewed the histogram badly enough
that Otsu classified the *entire real text region* as "black" — turning whole line-crop images into
solid black bars with no text visible at all.

**Round 3 — binarise before padding, and stop forcing one fixed canvas size.** The fix was to run
denoising and Otsu on the real resized image content first, and only pad the *already-binarised*
result onto the white canvas afterward — so Otsu never sees the padding pixels. On top of that, we
found the fixed `(800, 160)` canvas itself was a problem once we started testing with full-page
book/newspaper scans instead of just single cropped text lines: squeezing a tall portrait page into
a short, wide box crushed the whole page down to a sliver only ~15% of the canvas width, making the
text either illegibly tiny or, in pages with illustrations, collapsing the artwork into an unreadable
black blob. We replaced the fixed canvas with a simple bounded resize — only scale an image down if
it's larger than a max dimension, or up if it's smaller than a minimum, always preserving aspect
ratio, with no padding or forced canvas at all. That one change made the pipeline work for both the
single-line crops and the full-page scans without needing separate logic for each.