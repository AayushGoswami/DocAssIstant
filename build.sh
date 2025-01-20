#!/usr/bin/env bash

# Make the download script executable
chmod +x download_dll.sh

# Execute the download script
./download_dll.sh

# Install tesseract_ocr
sudo apt-get update && sudo apt-get install -y tesseract-ocr

# Continue with Python dependencies
pip install -r requirements.txt

# Add Tesseract to PATH
export PATH="/usr/bin/tesseract:$PATH"

which tesseract && tesseract --version
