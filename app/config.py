import os

class Settings:
    # Path configurations
    TESSERACT_PATH = '/usr/bin/tesseract'
    POPPLER_PATH = '/usr/bin'
    
    # Supported languages
    SUPPORTED_LANGUAGES = [
        'English',
        'Arabic',
        'French',
        'German',
        'Chinese'
    ]
    
    # Confidence thresholds
    CONFIDENCE_THRESHOLDS = {
        'low': 50,
        'medium': 70,
        'high': 90
    }

settings = Settings()
