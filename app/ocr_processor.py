import os
import io
import numpy as np
from PIL import Image
import pdf2image
import pytesseract
import easyocr
import requests
from paddleocr import PaddleOCR
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self):
        """Initialize OCR processors with fallback options"""
        self.easyocr_reader = None
        self.paddle_ocr = None
        self.use_native_tesseract = False
        
        try:
            # Initialize EasyOCR with limited languages to reduce memory usage
            self.easyocr_reader = easyocr.Reader(['en', 'ar'])
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize EasyOCR: {str(e)}")
        
        try:
            # Initialize PaddleOCR with reduced capabilities
            self.paddle_ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=False)
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize PaddleOCR: {str(e)}")
        
        # Check if native Tesseract is available
        try:
            pytesseract.get_tesseract_version()
            self.use_native_tesseract = True
            logger.info("Native Tesseract is available")
        except:
            logger.warning("Native Tesseract not available - using Tesseract fallback")

    def process_file(self, file_stream, file_extension: str, languages: List[str] = ['en'], **kwargs) -> Dict:
        """
        Process uploaded file and return OCR results
        
        Args:
            file_stream: Uploaded file stream
            file_extension: File extension (pdf, jpg, png)
            languages: List of languages to use for OCR
            
        Returns:
            Dictionary containing:
            - text: Combined OCR text
            - confidence: Average confidence score
            - words: List of words with confidence scores
            - languages: Detected languages
        """
        try:
            # Convert PDF to images or load single image
            if file_extension.lower() == 'pdf':
                images = self._convert_pdf_to_images(file_stream)
            else:
                images = [Image.open(file_stream)]
            
            results = []
            for img in images:
                results.append(self._process_image(img, languages, **kwargs))
            
            return self._combine_results(results)
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise

    def _convert_pdf_to_images(self, file_stream) -> List[Image.Image]:
        """Convert PDF to list of PIL images"""
        try:
            # Read PDF content
            pdf_bytes = file_stream.read()
            
            # Convert each page to image
            images = pdf2image.convert_from_bytes(
                pdf_bytes,
                dpi=300,
                fmt='jpeg',
                thread_count=2
            )
            return images
        except Exception as e:
            logger.error(f"PDF conversion failed: {str(e)}")
            raise

    def _process_image(self, image: Image.Image, languages: List[str], **kwargs) -> Dict:
        """Process single image with multiple OCR engines"""
        # Convert to OpenCV format if using OpenCV-based engines
        img_cv = None
        if self.easyocr_reader or self.paddle_ocr:
            img_cv = np.array(image)
            if len(img_cv.shape) == 2:  # Grayscale
                img_cv = np.stack((img_cv,)*3, axis=-1)
            elif img_cv.shape[2] == 4:  # RGBA
                img_cv = img_cv[:, :, :3]
        
        # Get results from all available engines
        engine_results = []
        
        # 1. Try EasyOCR first
        if self.easyocr_reader:
            try:
                easyocr_text, easyocr_conf = self._extract_with_easyocr(img_cv, languages)
                engine_results.append({
                    'engine': 'easyocr',
                    'text': easyocr_text,
                    'confidence': easyocr_conf
                })
            except Exception as e:
                logger.warning(f"EasyOCR failed: {str(e)}")
        
        # 2. Try PaddleOCR
        if self.paddle_ocr:
            try:
                paddle_text, paddle_conf = self._extract_with_paddleocr(img_cv)
                engine_results.append({
                    'engine': 'paddleocr',
                    'text': paddle_text,
                    'confidence': paddle_conf
                })
            except Exception as e:
                logger.warning(f"PaddleOCR failed: {str(e)}")
        
        # 3. Try native Tesseract
        try:
            tesseract_text, tesseract_conf = self._extract_with_tesseract(image, languages)
            engine_results.append({
                'engine': 'tesseract',
                'text': tesseract_text,
                'confidence': tesseract_conf
            })
        except Exception as e:
            logger.warning(f"Tesseract failed: {str(e)}")
        
        # Fallback to pytesseract if native not available
        if not engine_results:
            try:
                tesseract_text = pytesseract.image_to_string(image)
                engine_results.append({
                    'engine': 'pytesseract',
                    'text': tesseract_text,
                    'confidence': 0.7  # Default confidence
                })
            except Exception as e:
                logger.error(f"All OCR engines failed: {str(e)}")
                raise RuntimeError("All OCR engines failed to process the image")
        
        # Select best result (highest confidence)
        best_result = max(engine_results, key=lambda x: x['confidence'])
        
        return {
            'text': best_result['text'],
            'confidence': best_result['confidence'],
            'engine_used': best_result['engine'],
            'all_engines': engine_results
        }

    def _extract_with_easyocr(self, image: np.ndarray, languages: List[str]) -> Tuple[str, float]:
        """Extract text using EasyOCR"""
        # Convert language codes (e.g. 'en' -> 'english')
        lang_map = {'en': 'en', 'ar': 'ar', 'fr': 'fr', 'de': 'de', 'zh': 'ch_sim'}
        easyocr_langs = [lang_map.get(lang[:2].lower(), 'en') for lang in languages]
        
        result = self.easyocr_reader.readtext(image, detail=1)
        text = " ".join([entry[1] for entry in result])
        confidence = np.mean([entry[2] for entry in result]) if result else 0.5
        return text, float(confidence)

    def _extract_with_paddleocr(self, image: np.ndarray) -> Tuple[str, float]:
        """Extract text using PaddleOCR"""
        result = self.paddle_ocr.ocr(image, cls=False)
        if result and result[0]:
            text = " ".join([line[1][0] for line in result[0]])
            confidence = np.mean([line[1][1] for line in result[0]])
            return text, float(confidence)
        return "", 0.0

    def _extract_with_tesseract(self, image: Image.Image, languages: List[str]) -> Tuple[str, float]:
        """Extract text using Tesseract OCR"""
        # Map language codes to Tesseract format
        lang_map = {
            'en': 'eng',
            'ar': 'ara',
            'fr': 'fra',
            'de': 'deu',
            'zh': 'chi_sim'
        }
        tesseract_langs = "+".join([lang_map.get(lang[:2].lower(), 'eng') for lang in languages])
        
        # Get OCR data including confidence
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, lang=tesseract_langs)
        
        # Combine text with confidence > 60
        text = " ".join(
            word for word, conf in zip(data['text'], data['conf']) 
            if int(conf) > 60 and word.strip()
        )
        
        # Calculate average confidence (excluding -1 values)
        valid_confs = [c for c in data['conf'] if c != -1]
        avg_conf = np.mean(valid_confs) / 100 if valid_confs else 0.7
        
        return text, float(avg_conf)

    def _combine_results(self, page_results: List[Dict]) -> Dict:
        """Combine results from multiple pages"""
        combined_text = "\n\n".join([res['text'] for res in page_results])
        avg_confidence = np.mean([res['confidence'] for res in page_results])
        engines_used = list(set(res['engine_used'] for res in page_results))
        
        return {
            'text': combined_text,
            'confidence': avg_confidence,
            'engines_used': engines_used,
            'pages': len(page_results),
            'quality_report': self._generate_quality_report(page_results)
        }

    def _generate_quality_report(self, page_results: List[Dict]) -> Dict:
        """Generate quality assessment report"""
        word_counts = []
        confidences = []
        
        for page in page_results:
            word_counts.append(len(page['text'].split()))
            confidences.append(page['confidence'])
        
        return {
            'total_words': sum(word_counts),
            'avg_confidence': np.mean(confidences),
            'min_confidence': min(confidences),
            'max_confidence': max(confidences),
            'pages_processed': len(page_results)
        }

    def get_supported_languages(self) -> Dict[str, List[str]]:
        """Return supported languages for each engine"""
        return {
            'easyocr': ['en', 'ar', 'fr', 'de', 'zh'],
            'paddleocr': ['en', 'ch'],
            'tesseract': ['en', 'ar', 'fr', 'de', 'zh']
        }
