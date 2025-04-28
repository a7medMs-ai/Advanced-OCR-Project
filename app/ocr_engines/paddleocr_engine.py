from paddleocr import PaddleOCR
import cv2

def run_paddleocr(image, languages='en'):
    """
    Runs PaddleOCR on the given image and returns results.
    Each result contains:
    - text
    - confidence score
    - bounding box coordinates
    """
    # Initialize the PaddleOCR reader
    ocr = PaddleOCR(use_angle_cls=True, lang=languages, show_log=False)

    # Ensure the input image is in the correct format
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise ValueError(f"Could not load image at {image}")

    # Convert to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run PaddleOCR
    results_raw = ocr.ocr(rgb, cls=True)

    results = []
    for line in results_raw:
        for word_info in line:
            bbox, (text, confidence) = word_info
            if text.strip() != "":
                result = {
                    'text': text,
                    'confidence': round(confidence * 100, 2),  # Convert to percentage
                    'box': bbox
                }
                results.append(result)

    return results
