# app/processors/layout_detection.py

import layoutparser as lp
from PIL import Image
import os

def detect_layout(image_path, model_name='lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config', label_map=None):
    """
    Detect layout elements (tables, text blocks, figures) from an image.

    Args:
        image_path (str): Path to the image file.
        model_name (str): Pre-trained model URL from LayoutParser.
        label_map (dict): Custom label mapping for detected blocks (optional).

    Returns:
        list: List of dictionaries containing block information.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(image_path).convert('RGB')

    model = lp.Detectron2LayoutModel(
        model_name,
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
