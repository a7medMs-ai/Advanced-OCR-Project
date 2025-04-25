#!/bin/bash

echo "🚀 Starting setup..."

# Create virtual environment
python3 -m venv ocr_env

# Activate virtual environment
source ocr_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "✅ Setup completed! To activate environment later, run: source ocr_env/bin/activate"
