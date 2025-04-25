import pytesseract
import easyocr
from paddleocr import PaddleOCR
import pdf2image
import cv2
import numpy as np
from docx import Document
from openpyxl import Workbook
import pandas as pd
import os
from typing import Dict, List, Tuple
from PIL import Image
import re
from config import settings

class OCRProcessor:
    def __init__(self):
        self.easyocr_reader = easyocr.Reader(['en', 'ar'])
        self.paddle_ocr = PaddleOCR(use_angle_cls=True, lang='en')
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH
        self.poppler_path = settings.POPPLER_PATH
    
    def process_file(self, file_path: str, languages: List[str], **kwargs) -> Dict:
        """Process input file and return OCR results"""
        if file_path.lower().endswith('.pdf'):
            images = self._convert_pdf_to_images(file_path)
        else:
            images = [Image.open(file_path)]
        
        results = []
        for img in images:
            results.append(self._process_image(img, languages, **kwargs))
        
        final_result = self._combine_results(results)
        
        output_dir = os.path.join('data', 'output', os.path.splitext(os.path.basename(file_path))[0])
        os.makedirs(output_dir, exist_ok=True)
        
        docx_path = os.path.join(output_dir, 'output.docx')
        excel_path = os.path.join(output_dir, 'report.xlsx')
        quality_report_path = os.path.join(output_dir, 'quality_report.xlsx')
        
        self._save_to_docx(final_result['text'], docx_path)
        self._save_report_to_excel(final_result, excel_path)
        self._save_quality_report(final_result['quality_data'], quality_report_path)
        
        return {
            'text': final_result['text'],
            'quality_data': final_result['quality_data'],
            'quality_report': pd.DataFrame(final_result['quality_data']),
            'docx_path': docx_path,
            'excel_path': excel_path,
            'quality_report_path': quality_report_path
        }
    
    # ... [rest of the methods from previous implementation] ...
