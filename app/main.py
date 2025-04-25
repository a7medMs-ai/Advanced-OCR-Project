
### 3. app/main.py

```python
import streamlit as st
from ocr_processor import OCRProcessor
import os
import base64
from config import settings

def get_download_link(file_path, link_text):
    """Generate download link for files"""
    with open(file_path, "rb") as f:
        bytes_data = f.read()
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:file/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'
    return href

def main():
    st.set_page_config(page_title="Advanced OCR System", layout="wide")
    
    # Initialize OCR processor
    ocr_processor = OCRProcessor()
    
    st.title("Advanced OCR Processing System")
    st.markdown("""
    Combine multiple OCR engines with quality analysis and reporting
    """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload file (PDF, JPG, PNG)", type=["pdf", "jpg", "jpeg", "png"])
    
    # Language selection
    languages = st.multiselect(
        "Select document languages",
        options=settings.SUPPORTED_LANGUAGES,
        default=['English', 'Arabic']
    )
    
    # Processing options
    with st.expander("Advanced Options"):
        keep_formatting = st.checkbox("Preserve original formatting", value=True)
        analyze_tables = st.checkbox("Analyze tables separately", value=True)
        highlight_low_confidence = st.checkbox("Highlight low-confidence areas", value=True)
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner('Processing...'):
                try:
                    # Process file
                    result = ocr_processor.process_file(
                        uploaded_file,
                        languages=languages,
                        keep_formatting=keep_formatting,
                        analyze_tables=analyze_tables
                    )
                    
                    st.success("Processing completed successfully!")
                    
                    # Display results
                    st.subheader("Extracted Text")
                    st.text_area("OCR Result", value=result['text'], height=300)
                    
                    # Quality report
                    st.subheader("Quality Analysis")
                    st.dataframe(result['quality_report'])
                    
                    # Download links
                    st.subheader("Download Results")
                    st.markdown(get_download_link(result['docx_path'], 'Download Word Document'), unsafe_allow_html=True)
                    st.markdown(get_download_link(result['excel_path'], 'Download Excel Report'), unsafe_allow_html=True)
                    st.markdown(get_download_link(result['quality_report_path'], 'Download Quality Report'), unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")

if __name__ == "__main__":
    main()
