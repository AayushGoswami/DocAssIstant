#!/usr/bin/env bash
# Exit on error
set -e

# Create required directories with proper permissions
mkdir -p /opt/render/project/src/.apt/usr/share/doc
mkdir -p /opt/render/project/src/.apt/var/cache/apt/archives/partial
mkdir -p /opt/render/project/src/.apt/var/lib/apt/lists/partial

# Configure apt to use custom directories
echo 'Dir::Cache "/opt/render/project/src/.apt/var/cache/apt/";
Dir::Cache::archives "archives/";
Dir::State::lists "/opt/render/project/src/.apt/var/lib/apt/lists/";
Dir::State "/opt/render/project/src/.apt/var/lib/apt/";' > /opt/render/project/src/.apt/apt.conf

# Set environment variable to use custom apt configuration
export APT_CONFIG=/opt/render/project/src/.apt/apt.conf

# Update and install system dependencies
apt-get update -y
apt-get install -y tesseract-ocr
apt-get install -y libtesseract-dev

# Install Python dependencies
pip install -r requirements.txt
