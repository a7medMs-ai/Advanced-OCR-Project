from setuptools import setup, find_packages

setup(
    name="advanced-ocr",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.12.0",
        "pytesseract==0.3.10",
        "easyocr==1.6.2",
        "paddleocr==2.6.1.3",
        "pdf2image==1.16.3",
        "opencv-python-headless==4.6.0.66",
        "pillow==9.5.0",
        "python-docx==0.8.11",
        "openpyxl==3.1.2",
        "pandas==1.5.3",
        "numpy==1.24.3",
    ],
)
