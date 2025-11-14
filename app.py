import streamlit as st
import easyocr
import pdfplumber
import pandas as pd
import io
from PIL import Image


st.set_page_config(page_title="Extracteur d'enseignes PDF", page_icon="🛍️")
st.title("🛍️ Extracteur d’Enseignes OCR depuis un PDF")
st.markdown("**Dépose ton fichier PDF contenant les enseignes (scannés ou non), traitement avec EasyOCR, et récupère un fichier Excel propre.**")

uploaded_file = st.file_uploader("📤 Upload ton fichier PDF ici", type="pdf")

if uploaded_file is not None:
    with st.spinner("🔎 Lecture et extraction OCR en cours..."):
        enseignes = []
        reader = easyocr.Reader(['fr'], gpu=False)
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                # Crop à gauche si besoin (adapter selon le PDF)
                cropped = page.crop((75, 0, page.width, page.height))
                img = cropped.to_image(resolution=300).original
                img_pil = Image.fromarray(img)
                
                # Passage OCR
                results = reader.readtext(img_pil, detail=0)
                for enseigne in results:
                    enseigne_clean = enseigne.strip().upper()
                    if len(enseigne_clean) > 1:
                        enseignes.append(enseigne_clean)

        enseignes_uniques = sorted(set(enseignes))
        df = pd.DataFrame(enseignes_uniques, columns=["Enseigne extraite (OCR)"])
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)

        st.success(f"✅ Extraction OCR réussie : {len(df)} enseignes trouvées")
        st.download_button(
            label="📥 Télécharger le fichier Excel",
            data=excel_buffer,
            file_name="enseignes_nettoyees_OCR.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
