#!/bin/bash

# Create directory if it doesn't exist
mkdir -p utils/OCR/Tesseract-OCR

# Download the file

https://drive.google.com/file/d/1HgxAEzr6SHB8wZpfwX5DBKsgKAoDaZY9/view?usp=sharing

wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1HgxAEzr6SHB8wZpfwX5DBKsgKAoDaZY9' -O utils/OCR/Tesseract-OCR/libicudt75.dll

# Check if download was successful
if [ -f "utils/OCR/Tesseract-OCR/libicudt75.dll" ]; then
    echo "DLL file downloaded successfully"
else
    echo "Error downloading DLL file"
    exit 1
fi
