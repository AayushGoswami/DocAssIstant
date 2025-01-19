#!/usr/bin/env bash

# Make the download script executable
chmod +x download_dll.sh

# Execute the download script
./download_dll.sh

# Install tesseract_ocr
apt-get update && apt-get install -y tesseract-ocr

# Continue with Python dependencies
pip install -r requirements.txt
