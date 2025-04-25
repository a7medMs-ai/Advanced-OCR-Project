# app/ocr_engines/tesseract_engine.py

import pytesseract
from PIL import Image

def extract_text_tesseract(image_path, languages=['en']):
    """
    Extract text from an image using Tesseract OCR.

    Args:
        image_path (str): Path to the input image.
        languages (list): List of language codes. Example: ['en'], ['ar'], ['en', 'ar']

    Returns:
        str: Extracted text.
    """
    try:
        img = Image.open(image_path)
    except Exception as e:
        raise Exception(f"Error opening image: {e}")

    lang_str = '+'.join(languages) if languages else 'eng'

    try:
        text = pytesseract.image_to_string(img, lang=lang_str)
    except Exception as e:
        raise Exception(f"Tesseract OCR failed: {e}")

    return text
