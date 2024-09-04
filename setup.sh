#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.8 or newer."
    exit 1
fi

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt

pip install nltk

# Download additional resources, if needed
echo "Downloading necessary resources..."
python3 -m nltk.downloader punkt

# Setup is complete
echo "Setup complete. Activate the virtual environment with 'source venv/bin/activate' and run your scripts."
