# app/processors/image_preprocessing.py

import cv2
import numpy as np
from PIL import Image
import os

def preprocess_image(image_path, output_path=None):
    """
    Preprocess the image for better OCR results:
    - Convert to grayscale
    - Apply adaptive thresholding
    - Denoise
    - Sharpen edges

    Args:
        image_path (str): Path to input image.
        output_path (str, optional): Path to save the preprocessed image. If None, does not save.

    Returns:
        PIL.Image: Preprocessed image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 
        11, 2
    )

    # Denoise
    denoised = cv2.fastNlMeansDenoising(thresh, h=30)

    # Sharpening
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    # Convert back to PIL
    preprocessed_pil = Image.fromarray(sharpened)

    # Save if required
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        preprocessed_pil.save(output_path)

    return preprocessed_pil
