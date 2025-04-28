import streamlit as st
import os
import tempfile
from processors.image_preprocessing import preprocess_image
from processors.pdf_processor import pdf_to_images
from ocr_engines.tesseract_engine import run_tesseract_ocr
from ocr_engines.easyocr_engine import run_easyocr
from ocr_engines.paddleocr_engine import run_paddleocr
from utils.confidence_highlighter import create_highlighted_document

def main():
    st.title("Advanced OCR System with Confidence Highlighting")

    uploaded_file = st.file_uploader("Upload an image or PDF", type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, uploaded_file.name)

            with open(input_path, 'wb') as f:
                f.write(uploaded_file.read())

            images = []
            if file_extension == 'pdf':
                images = pdf_to_images(input_path, temp_dir)
            else:
                images = [input_path]

            all_results = []

            st.info("Processing files...")

            for img_path in images:
                preprocessed_img = preprocess_image(img_path)

                tesseract_results = run_tesseract_ocr(preprocessed_img)
                easyocr_results = run_easyocr(preprocessed_img)
                paddleocr_results = run_paddleocr(preprocessed_img, languages='en')

                combined_results = tesseract_results + easyocr_results + paddleocr_results

                all_results.extend(combined_results)

            st.success("OCR completed successfully.")

            if all_results:
                output_word_path = os.path.join(temp_dir, "output.docx")

                rtl_mode = st.checkbox("RTL Mode (Arabic)", value=True)

                create_highlighted_document(all_results, output_word_path, rtl=rtl_mode)

                with open(output_word_path, "rb") as file:
                    st.download_button(
                        label="Download Result as Word Document",
                        data=file,
                        file_name="ocr_output.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

if __name__ == "__main__":
    main()
