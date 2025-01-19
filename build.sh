#!/usr/bin/env bash

# Make the download script executable
chmod +x download_dll.sh

# Execute the download script
./download_dll.sh

# Continue with your existing build steps
apt-get update

# Continue with Python dependencies
pip install -r requirements.txt
