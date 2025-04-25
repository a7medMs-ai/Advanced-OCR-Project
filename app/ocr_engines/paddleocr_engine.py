# app/ocr_engines/paddleocr_engine.py

from paddleocr import PaddleOCR

# Cache for PaddleOCR instances
_paddleocr_readers = {}

def extract_text_paddleocr(image_path, languages=['en']):
    """
    Extract text from an image using PaddleOCR.

    Args:
        image_path (str): Path to the input image.
        languages (list): List of language codes. Example: ['en'], ['ar'], ['en', 'ar']

    Returns:
        str: Extracted text.
    """
    lang_key = '_'.join(languages)

    if lang_key not in _paddleocr_readers:
        # Default to English model
        use_angle_cls = True
        lang_model = 'en' if 'ar' not in languages else 'ar'

        _paddleocr_readers[lang_key] = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang_model)

    ocr = _paddleocr_readers[lang_key]
    result = ocr.ocr(image_path, cls=True)

    texts = []
    for line in result:
        if line:
            for word_info in line:
                word = word_info[1][0]
                texts.append(word)

    return "\n".join(texts)
