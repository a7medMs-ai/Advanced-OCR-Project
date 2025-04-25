# app/main.py

import os
import streamlit as st
from app.processors.image_preprocessing import preprocess_image
from app.ocr_engines.ensemble_ocr import ensemble_ocr
from app.output.docx_writer import create_docx_from_text

SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
SUPPORTED_PDF_FORMATS = ['.pdf']

def process_folder(input_folder, output_folder, language='en'):
    """
    Process all supported files in the input folder and generate DOCX files.

    Args:
        input_folder (str): Path to folder containing images or PDFs.
        output_folder (str): Path to folder where outputs will be saved.
        language (str): Language for OCR.
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
            st.write(f"PDF support will be added in next version: {filename}")
            # Future work: Convert PDF to images then OCR

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
        else:
            st.error("Please specify both input and output folders.")

if __name__ == "__main__":
    main()
