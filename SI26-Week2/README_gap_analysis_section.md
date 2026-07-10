## Why We Need a Better Model

We ran baseline [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (with the `urd` language pack)
on 5 preprocessed images from our dataset to establish a baseline and understand the gap our
custom model needs to close.

### Results

| Image | Actual Urdu Text | Tesseract Output | What Went Wrong |
|---|---|---|---|
| image_1.png | *(fill in)* | *(fill in)* | *(fill in)* |
| image_2.png | | | |
| image_3.png | | | |
| image_4.png | | | |
| image_5.png | | | |

### Summary

> Tesseract fails on Urdu because ... *(finish based on your actual results — consider: Nastaliq's
> cursive, position-dependent letter shapes vs. Tesseract's Naskh-trained model; right-to-left
> word segmentation; loss of diacritics/dots during binarisation; ligature/character merging.)*

### Preprocessing note

An earlier version of our preprocessing pipeline used a fixed global brightness threshold
(`cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)`), which produced speckled/"dotted" output on
images with uneven lighting, since a single cutoff value can't handle shadowed regions correctly.
We switched to **Otsu's method** (`cv2.THRESH_OTSU`), which computes the optimal threshold
per image automatically, and switched from a hard resize to an aspect-ratio-preserving
resize with padding to avoid warping character shapes. This produced clean binarised output
suitable for OCR testing.
