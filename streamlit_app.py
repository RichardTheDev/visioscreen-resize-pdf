import streamlit as st
from pdf2image import convert_from_bytes
import io
from zipfile import ZipFile, ZIP_DEFLATED

# Fonction pour redimensionner une image selon les dimensions souhaitées
def resize_image(image, desired_width, desired_height):
    return image.resize((desired_width, desired_height))

# Fonction pour créer un fichier ZIP des images redimensionnées et générer un lien de téléchargement
def create_download_zip(images, prefix="pages"):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'a') as zip_file:
        for i, image in enumerate(images, start=1):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            zip_file.writestr(f"{prefix}_page_{i}.png", img_byte_arr, compress_type=ZIP_DEFLATED)
    zip_buffer.seek(0)
    return zip_buffer

def main():
    st.title("Convertisseur PDF en PNG et redimensionnement")
    st.subheader("By Visioscreen")

    uploaded_pdfs = st.file_uploader("Téléchargez un ou plusieurs fichiers PDF", type="pdf", accept_multiple_files=True)

    if uploaded_pdfs:
        desired_width = st.number_input("Entrez la largeur souhaitée en pixels", value=600, step=100)
        desired_height = st.number_input("Entrez la hauteur souhaitée en pixels", value=800, step=100)

        if st.button("Traiter les PDF et Télécharger le ZIP"):
            all_images = []
            for uploaded_pdf in uploaded_pdfs:
                uploaded_pdf.seek(0)
                images = convert_from_bytes(uploaded_pdf.read())

                for image in images:
                    resized_image = resize_image(image, desired_width, desired_height)
                    all_images.append(resized_image)

            # Créer un fichier ZIP avec toutes les images redimensionnées
            zip_buffer = create_download_zip(all_images, "all_pages")
            st.download_button(label="Télécharger toutes les images en ZIP",
                               data=zip_buffer,
                               file_name="all_pages_resized.zip",
                               mime="application/zip")

if __name__ == "__main__":
    st.markdown("""
                    <style>
                    .stActionButton {visibility: hidden;}
                    /* Hide the Streamlit footer */
                    .reportview-container .main footer {visibility: hidden;}
                    /* Additionally, hide Streamlit's hamburger menu - optional */
                    .sidebar .sidebar-content {visibility: hidden;}
                    </style>
                    """, unsafe_allow_html=True)
    main()
