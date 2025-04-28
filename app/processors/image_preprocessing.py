import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Preprocess the input image to enhance OCR accuracy.
    Steps:
    - Convert to grayscale
    - Remove noise
    - Apply thresholding
    - Deskew the image
    - Sharpen edges
    """
    # Read the image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not read the image at path: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to remove noise while keeping edges sharp
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )

    # Deskew the image
    deskewed = deskew(thresh)

    # Sharpen the image
    sharpened = sharpen_image(deskewed)

    return sharpened

def deskew(image):
    """
    Corrects skew in the image using image moments.
    """
    coords = np.column_stack(np.where(image > 0))
    if coords.shape[0] == 0:
        return image  # No text detected

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, 
                             borderMode=cv2.BORDER_REPLICATE)

    return rotated

def sharpen_image(image):
    """
    Sharpens the image to make text edges clearer.
    """
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened
