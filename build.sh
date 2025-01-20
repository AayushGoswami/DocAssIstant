#!/usr/bin/env bash

# Make the download script executable
# chmod +x download_dll.sh

# # Execute the download script
# ./download_dll.sh

# Install tesseract_ocr
sudo apt-get update

# Install tesseract-ocr and its dependencies
sudo apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    python3-pip


# Continue with Python dependencies
pip install -r requirements.txt

# Add Tesseract to PATH
echo 'export PATH="/usr/bin/tesseract:$PATH"' >> ~/.bashrc

# Create symlink to ensure tesseract is accessible
ln -s /usr/bin/tesseract /usr/local/bin/tesseract

# Reload bash profile to apply PATH changes
source ~/.bashrc

# Verify installation
tesseract --version
python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"
