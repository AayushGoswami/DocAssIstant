#!/bin/bash

# Install tesseract-ocr and its dependencies
sudo apt-get update && sudo apt-get install -y tesseract-ocr && sudo apt-get install -y libtesseract-dev && sudo apt-get install -y libleptonica-dev && sudo apt-get install -y pkg-config

# Continue with Python dependencies
pip install -r requirements.txt

# Add Tesseract to PATH
export PATH="/usr/bin/tesseract:$PATH"

# Create symlink to ensure tesseract is accessible
ln -s /usr/bin/tesseract /usr/local/bin/tesseract

# Verify installation
which tesseract && tesseract --version
python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"
