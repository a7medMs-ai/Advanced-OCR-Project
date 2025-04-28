import pytesseract
import cv2

def run_tesseract_ocr(image, lang='eng+ara'):
    """
    Runs Tesseract OCR on the given image and returns results.
    Each result contains:
    - text
    - confidence score
    - bounding box coordinates
    """
    # Ensure the input image is in the correct format
    if isinstance(image, str):
        image = cv2.imread(image)
        if image is None:
            raise ValueError(f"Could not load image at {image}")

    # Convert to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run Tesseract OCR
    data = pytesseract.image_to_data(
        rgb,
        output_type=pytesseract.Output.DICT,
        lang=lang,
        config='--oem 3 --psm 6'
    )

    results = []
    for i in range(len(data['text'])):
        text = data['text'][i]
        conf = int(data['conf'][i])

        if text.strip() != "":
            result = {
                'text': text,
                'confidence': conf,
                'box': (
                    data['left'][i],
                    data['top'][i],
                    data['width'][i],
                    data['height'][i]
                )
            }
            results.append(result)

    return results
