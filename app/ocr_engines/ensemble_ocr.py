
# app/ocr_engines/ensemble_ocr.py

import os
from app.ocr_engines.tesseract_engine import extract_text_tesseract
from app.ocr_engines.easyocr_engine import extract_text_easyocr
from app.ocr_engines.paddleocr_engine import extract_text_paddleocr

def ensemble_ocr(image_path, languages=['en']):
    """
    Apply multiple OCR engines on the input image and merge results.

    Args:
        image_path (str): Path to the image file.
        languages (list): Languages to recognize. Example: ['en'], ['ar'], ['en', 'ar']

    Returns:
        str: Final improved text.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Extract text from multiple engines
    text_tesseract = extract_text_tesseract(image_path, languages)
    text_easyocr = extract_text_easyocr(image_path, languages)
    text_paddleocr = extract_text_paddleocr(image_path, languages)

    candidates = [text_tesseract, text_easyocr, text_paddleocr]

    # Use majority voting to choose the most consistent text
    final_text = majority_vote(candidates)
    return final_text

def majority_vote(text_list):
    """
    Choose the text that appears most among the results.

    Args:
        text_list (list): List of OCR results.

    Returns:
        str: The most voted text.
    """
    from collections import Counter

    clean_texts = [text.strip() for text in text_list if text.strip()]
    if not clean_texts:
        return ""

    count = Counter(clean_texts)
    most_common_text, freq = count.most_common(1)[0]
    return most_common_text
