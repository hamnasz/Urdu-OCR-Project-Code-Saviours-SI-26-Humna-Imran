import streamlit as st
from PIL import Image
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

st.set_page_config(page_title="Urdu OCR — Code Saviours SI-26", page_icon="📝", layout="centered")

# --- Point this at your model -------------------------------------------------
# Option A (recommended): push your trained model to the Hugging Face Hub as a
# MODEL repo (not a Space) and load it by id. Avoids committing a ~1GB+ file to
# GitHub and avoids Git LFS entirely.
#   from huggingface_hub import HfApi
#   api = HfApi()
#   api.create_repo("your-username/urdu-ocr-si26", repo_type="model")
#   model.push_to_hub("your-username/urdu-ocr-si26")
#   processor.push_to_hub("your-username/urdu-ocr-si26")
MODEL_ID = "your-hf-username/urdu-ocr-si26"  # <-- replace after pushing to the Hub

# Option B: if you'd rather load straight from a path inside your repo (requires
# Git LFS for the model weights, since data/model isn't tracked by a plain git push),
# swap MODEL_ID above for a relative path from your repo root, e.g.:
#   MODEL_ID = "SI26-Week1/data/model"
# -------------------------------------------------------------------------------

MAX_LENGTH = 128


@st.cache_resource(show_spinner=False)
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = TrOCRProcessor.from_pretrained(MODEL_ID)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_ID).to(device)
    model.eval()
    return processor, model, device


st.title("Urdu OCR")
st.caption("Fine-tuned TrOCR model — Code Saviours ML/AI Internship, Batch SI-26")

with st.spinner("Loading model (first run only, can take a minute)..."):
    try:
        processor, model, device = load_model()
    except Exception as e:
        st.error(
            "Couldn't load the model. Check that MODEL_ID at the top of app.py "
            f"points at a valid, public model repo. Details: {e}"
        )
        st.stop()

uploaded = st.file_uploader("Upload an image containing Urdu text", type=["png", "jpg", "jpeg"])

if uploaded is not None:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Uploaded image", use_container_width=True)

    with st.spinner("Extracting text..."):
        pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
        with torch.no_grad():
            generated_ids = model.generate(pixel_values, max_length=MAX_LENGTH)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    st.subheader("Extracted Text")
    if text:
        st.markdown(
            f'<div dir="rtl" lang="ur" style="font-size:1.5rem; line-height:2.1; '
            f'padding:1rem 1.25rem; border:1px solid #444; border-radius:8px;">{text}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning("Could not extract text from this image.")
else:
    st.info("Upload a JPG or PNG with Urdu text to get started.")

st.divider()
st.caption("Built during the Code Saviours ML/AI Internship — Batch SI-26.")
