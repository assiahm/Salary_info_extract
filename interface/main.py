import streamlit as st
from app.ingestion import load_file
from app.ocr import apply_ocr
from app.classifier import classify_text
from app.extractor import extract_entities
from app.formatter import to_json, to_csv
from app.logger import setup_logger

logger = setup_logger()

st.title("Extraction automatique de documents")
uploaded_file = st.file_uploader("Charger un document", type=["pdf", "png", "jpg"])

if uploaded_file:
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.read())
    logger.info("Fichier chargé")

    images = load_file("temp_file")
    text_pages = apply_ocr(images)
    full_text = "\n".join(text_pages)

    doc_type = classify_text(full_text)
    st.write(f"Type de document : {doc_type}")

    extracted_data = extract_entities(full_text)
    st.json(extracted_data)

    to_json(extracted_data, "output.json")
    to_csv(extracted_data, "output.csv")
    st.success("Export JSON et CSV effectué")
