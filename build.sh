#!/usr/bin/env bash
# Exit on error
set -e

# Install system dependencies
apt-get update -y
apt-get install -y tesseract-ocr
apt-get install -y libtesseract-dev

# Install Python dependencies
pip install -r requirements.txt
