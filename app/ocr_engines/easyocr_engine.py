# app/ocr_engines/easyocr_engine.py

import easyocr

# Create a cache for EasyOCR readers to avoid reloading models
_easyocr_readers = {}

def extract_text_easyocr(image_path, languages=['en']):
    """
    Extract text from an image using EasyOCR.

    Args:
        image_path (str): Path to the input image.
        languages (list): List of language codes. Example: ['en'], ['ar'], ['en', 'ar']

    Returns:
        str: Extracted text.
    """
    lang_str = [lang.lower() for lang in languages]
    lang_key = '_'.join(lang_str)

    if lang_key not in _easyocr_readers:
        _easyocr_readers[lang_key] = easyocr.Reader(lang_str, gpu=False)

    reader = _easyocr_readers[lang_key]
    result = reader.readtext(image_path, detail=0)  # Only text, not boxes

    return "\n".join(result)
