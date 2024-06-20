#!/bin/bash

# Update and install dependencies
sudo apt update
sudo apt install -y python3-pip python3-nautilus mediainfo libmediainfo-dev

# Install necessary Python packages
pip3 install pymediainfo

# Create necessary directories
mkdir -p ~/.local/share/nautilus-python/extensions/

# Copy the extension script to the appropriate location
cp nautilus-python/extensions/video_duration.py ~/.local/share/nautilus-python/extensions/

# Ensure the script is executable
chmod +x ~/.local/share/nautilus-python/extensions/video_duration.py

# Restart Nautilus to apply changes
nautilus -q

echo "Nautilus video duration extension installed successfully. Please reopen your file manager."
