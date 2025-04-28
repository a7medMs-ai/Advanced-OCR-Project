import easyocr
import cv2

def run_easyocr(image, languages=['en', 'ar']):
    """
    Runs EasyOCR on the given image and returns results.
    Each result contains:
    - text
    - confidence score
    - bounding box coordinates
    """
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(languages, gpu=False)

    # Ensure the input image is in the correct format
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise ValueError(f"Could not load image at {image}")

    # Convert to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run EasyOCR
    detections = reader.readtext(rgb)

    results = []
    for detection in detections:
        bbox, text, confidence = detection
        if text.strip() != "":
            result = {
                'text': text,
                'confidence': round(confidence * 100, 2),  # Convert to percentage
                'box': bbox  # bounding box points
            }
            results.append(result)

    return results
