import streamlit as st
import pdfplumber
import pandas as pd
import io

st.set_page_config(page_title="Extracteur d'enseignes PDF", page_icon="🛍️")

st.title("🛍️ Extracteur d’Enseignes depuis un PDF")
st.markdown("**Dépose ton fichier PDF contenant les enseignes (type plan de centre commercial), et récupère un fichier Excel propre.**")

uploaded_file = st.file_uploader("📤 Upload ton fichier PDF ici", type="pdf")

if uploaded_file is not None:
    with st.spinner("🔎 Lecture et extraction en cours..."):
        enseignes = []

        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                cropped = page.crop((0, 0, page.width * 0.2, page.height))
                table = cropped.extract_table()
                if table:
                    for row in table:
                        if row and row[0]:
                            texte = row[0].strip()
                            if len(texte) > 1:
                                enseignes.append(texte.upper())

        enseignes_uniques = sorted(set(enseignes))
        df = pd.DataFrame(enseignes_uniques, columns=["Enseigne extraite"])

        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)

        st.success(f"✅ Extraction réussie : {len(df)} enseignes trouvées")
        st.download_button(
            label="📥 Télécharger le fichier Excel",
            data=excel_buffer,
            file_name="enseignes_extraites.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
