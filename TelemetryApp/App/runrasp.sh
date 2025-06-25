#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create the virtual environment
echo "Creating virtual environment..."
python3 -m venv /home/user/App/venv

# Activate the virtual environment
echo "Activating virtual environment..."
source /home/user/App/venv/bin/activate

# Ensure pip is installed and upgraded
echo "Ensuring pip is installed..."
python -m ensurepip --upgrade

# Install dependencies
echo "Installing dependencies"
pip install -r /home/user/App/requirements.txt

# Run the application
echo "Running your application..."
python /home/user/App/app.py

# Keep the terminal open after running
read -p "Press enter to exit..."