import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.ingestion import load_file
from app.ocr import apply_ocr
from app.classifier import classify_text
from app.extractor import extract_entities
from app.formatter import to_json, to_csv
from app.logger import setup_logger

import os
from datetime import datetime

logger = setup_logger()

st.set_page_config(page_title="Analyse de documents salariaux", layout="centered")

st.title("📄 Analyse automatique de documents financiers")

st.markdown("""
Ce service permet d’analyser automatiquement des documents tels que :  
- Bulletins de paie  
- Certificats de salaire  
- Relevés bancaires  

Les informations extraites sont affichées ci-dessous et exportables au format JSON/CSV.
""")

uploaded_file = st.file_uploader("📁 Charger un fichier PDF ou image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    # Sauvegarde temporaire du fichier
    temp_path = f"temp_upload_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    logger.info("Fichier reçu et enregistré localement.")

    # Étape 1 : OCR
    try:
        images = load_file(temp_path)
        text_pages = apply_ocr(images)
        full_text = "\n".join(text_pages)

        # Étape 2 : Classification
        doc_type = classify_text(full_text)
        st.subheader("📄 Type de document détecté :")
        st.success(doc_type)

        # Étape 3 : Extraction
        extracted_data = extract_entities(full_text)
        st.subheader("🔍 Données extraites :")
        st.json(extracted_data)

        # Étape 4 : Export JSON / CSV
        output_name = os.path.splitext(uploaded_file.name)[0]
        json_path = f"{output_name}.json"
        csv_path = f"{output_name}.csv"
        to_json(extracted_data, json_path)
        to_csv(extracted_data, csv_path)

        with open(json_path, "rb") as f:
            st.download_button("⬇️ Télécharger le JSON", f, file_name=json_path, mime="application/json")
        with open(csv_path, "rb") as f:
            st.download_button("⬇️ Télécharger le CSV", f, file_name=csv_path, mime="text/csv")

        logger.info("Traitement terminé avec succès.")
        os.remove(temp_path)
    except Exception as e:
        st.error(f"Erreur durant le traitement : {e}")
        logger.error(f"Erreur : {e}")
