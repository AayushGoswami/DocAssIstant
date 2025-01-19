#!/usr/bin/env bash

# Make the download script executable
chmod +x download_dll.sh

# Execute the download script
./download_dll.sh

# Install tesseract_ocr
sudo apt-get update && sudo apt-get install -y tesseract-ocr
which tesseract && tesseract --version

# Continue with Python dependencies
pip install -r requirements.txt
