#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create the virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Ensure pip is installed and upgraded
echo "Ensuring pip is installed..."
python -m ensurepip --upgrade

# Install dependencies from the local packages folder (offline)
echo "Installing dependencies from local packages..."
pip install --find-links=packages -r requirements.txt

# Run the application
echo "Running your application..."
python app.py

# Keep the terminal open after running
read -p "Press enter to exit..."