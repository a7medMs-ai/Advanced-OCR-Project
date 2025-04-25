# app/main.py

import os
import shutil
import zipfile
import streamlit as st
from processors.image_preprocessing import preprocess_image
from app.ocr_engines.ensemble_ocr import ensemble_ocr
from app.output.docx_writer import create_docx_from_text

SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
SUPPORTED_PDF_FORMATS = ['.pdf']

def process_folder(input_folder, output_folder, language='en'):
    """
    Process all supported files in the input folder and generate DOCX files.
    """
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(input_folder)
    for filename in files:
        file_path = os.path.join(input_folder, filename)
        name, ext = os.path.splitext(filename)

        if ext.lower() in SUPPORTED_IMAGE_FORMATS:
            st.write(f"Processing image: {filename}")
            preprocessed_image = preprocess_image(file_path)
            temp_path = f"temp/{name}_preprocessed.png"
            os.makedirs("temp", exist_ok=True)
            preprocessed_image.save(temp_path)

            extracted_text = ensemble_ocr(temp_path, languages=[language])
            output_docx_path = os.path.join(output_folder, f"{name}.docx")
            create_docx_from_text(extracted_text, output_docx_path, language=language)

        elif ext.lower() in SUPPORTED_PDF_FORMATS:
            st.write(f"PDF support will be added soon: {filename}")

def zip_folder(folder_path, zip_path):
    """
    Compress a folder into a ZIP file.

    Args:
        folder_path (str): Path to folder.
        zip_path (str): Path to output ZIP file.
    """
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', folder_path)

def main():
    st.title("Advanced OCR Batch Processing Tool")

    st.sidebar.header("Upload Folder")

    input_folder = st.sidebar.text_input("Input Folder Path")
    output_folder = st.sidebar.text_input("Output Folder Path")
    language = st.sidebar.selectbox("Select Language", ['en', 'ar'])

    if st.sidebar.button("Start OCR"):
        if input_folder and output_folder:
            st.info(f"Processing all files from {input_folder}...")
            process_folder(input_folder, output_folder, language=language)
            st.success("Processing Completed! Check your output folder.")

            # After processing, create a ZIP and provide download
            zip_path = "output_results.zip"
            zip_folder(output_folder, zip_path)

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download All DOCX Files (ZIP)",
                    data=f,
                    file_name="output_results.zip",
                    mime="application/zip"
                )
        else:
            st.error("Please specify both input and output folders.")

if __name__ == "__main__":
    main()
