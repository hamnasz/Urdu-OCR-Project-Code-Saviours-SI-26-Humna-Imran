"""
Organise Week 1 raw data into the required SI26-Week1/data/raw/ structure.

WHAT THIS DOES
--------------
1. Extracts book.zip / newspaper.zip / signboard.zip (only if not already
   extracted) into their matching *_extract folders inside Other/.
2. Copies images from each source folder into the correct category under
   data/raw/ (books, newspaper, other) -- the data/ path itself is left
   exactly as-is, per the requirement.
3. Any file that isn't a valid, openable image -- wrong extension, corrupt,
   a stray .DS_Store, whatever -- is automatically routed to data/raw/other/
   instead of breaking the run. That's the "useless files go to other"
   behaviour you asked for.

HOW TO USE
----------
Paste the code below (everything after the docstring) into a new cell in
SI26_Week1_humna.ipynb, OR run this file directly with:
    python organise_week1_data.py
from wherever SI26-Week1/ lives (repo root or one level up -- same
auto-detection logic as your Week 2 notebook).

ASSUMPTIONS -- CHECK THESE BEFORE RUNNING
------------------------------------------
- Folder is named "SI26-Week1" (matches your Week 2 notebook's BASE).
  If yours is literally "S126-Week1" (with a 1), change BASE below.
- signboard_extract has no dedicated category yet, so it's mapped to
  "other" for now -- change SOURCE_TO_CATEGORY if you'd rather give
  signboards their own folder under data/raw/.
- Existing filenames in the destination are never overwritten; a
  collision gets the source-folder name appended instead.
"""

import os
import shutil
import zipfile
from PIL import Image

# ---- Configure paths -------------------------------------------------
if os.path.exists('SI26-Week1/Other'):
    BASE = 'SI26-Week1'
elif os.path.exists('../SI26-Week1/Other'):
    BASE = '../SI26-Week1'
else:
    raise FileNotFoundError(
        'Could not find SI26-Week1/Other. Check the folder name/location, '
        'or edit BASE at the top of this script directly.'
    )

OTHER_DIR = f'{BASE}/Other'      # where your zips / extracted folders currently sit
RAW_DIR = f'{BASE}/data/raw'     # required destination structure -- unchanged

VALID_EXTS = {'.jpg', '.jpeg', '.png'}

# source folder (after extraction) -> destination category under data/raw/
SOURCE_TO_CATEGORY = {
    'book_extract': 'books',
    'newspaper_extract': 'newspaper',
    'utrset_real_download': 'other',   # matches Week 2's "other" = UTRSet
    'signboard_extract': 'other',      # no dedicated category yet
}

# zip filename -> extract folder it should unzip into (skipped if already extracted)
ZIP_TO_EXTRACT_DIR = {
    'book.zip': 'book_extract',
    'newspaper.zip': 'newspaper_extract',
    'signboard.zip': 'signboard_extract',
}


def ensure_extracted():
    """Unzip anything in OTHER_DIR that hasn't been extracted yet."""
    for zip_name, extract_name in ZIP_TO_EXTRACT_DIR.items():
        zip_path = os.path.join(OTHER_DIR, zip_name)
        extract_path = os.path.join(OTHER_DIR, extract_name)
        if os.path.exists(zip_path) and not os.path.isdir(extract_path):
            print(f'Extracting {zip_name} -> {extract_name}/')
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_path)
        elif os.path.isdir(extract_path):
            print(f'{extract_name}/ already exists, skipping extraction')


def organise():
    for cat in set(SOURCE_TO_CATEGORY.values()) | {'other'}:
        os.makedirs(os.path.join(RAW_DIR, cat), exist_ok=True)

    moved, junked = 0, 0
    for source_folder, category in SOURCE_TO_CATEGORY.items():
        src_path = os.path.join(OTHER_DIR, source_folder)
        if not os.path.isdir(src_path):
            print(f'Skipping missing folder: {src_path}')
            continue

        for fname in os.listdir(src_path):
            fpath = os.path.join(src_path, fname)
            if not os.path.isfile(fpath):
                continue

            ext = os.path.splitext(fname)[1].lower()
            dest_category = category

            # Safety net: even inside a "known" folder, verify the file is
            # really a readable image. Anything broken/unexpected falls back
            # to data/raw/other/ instead of silently corrupting the dataset.
            is_valid_image = ext in VALID_EXTS
            if is_valid_image:
                try:
                    with Image.open(fpath) as im:
                        im.verify()
                except Exception:
                    is_valid_image = False

            if not is_valid_image:
                dest_category = 'other'
                junked += 1

            dest_path = os.path.join(RAW_DIR, dest_category, fname)
            if os.path.exists(dest_path):
                base, ext2 = os.path.splitext(fname)
                dest_path = os.path.join(RAW_DIR, dest_category, f'{base}_{source_folder}{ext2}')

            shutil.copy2(fpath, dest_path)
            moved += 1

    print(f'Organised {moved} files into {RAW_DIR}/  '
          f'({junked} unreadable/non-image files routed to other/)')


ensure_extracted()
organise()
