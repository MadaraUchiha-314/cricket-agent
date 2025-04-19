#!/usr/bin/env python3
import os
import csv
import json
import shutil
import zipfile
import requests
from pathlib import Path

# URLs for data sources
MATCHES_URL = "https://cricsheet.org/downloads/all_json.zip"
PEOPLE_URL = "https://cricsheet.org/register/people.csv"

# Paths
DATA_STORE_DIR = Path("data-store")
MATCHES_DIR = DATA_STORE_DIR / "matches"
PEOPLE_CSV = DATA_STORE_DIR / "people.csv"
TEMP_ZIP = DATA_STORE_DIR / "all_json.zip"

def ensure_directories():
    """Create necessary directories if they don't exist."""
    DATA_STORE_DIR.mkdir(exist_ok=True)
    MATCHES_DIR.mkdir(exist_ok=True)

def download_file(url, destination):
    """Download a file from a URL to the specified destination."""
    print(f"Downloading {url} to {destination}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Downloaded {destination}")

def download_and_extract_matches():
    """Download and extract match data."""
    # Download the ZIP file
    download_file(MATCHES_URL, TEMP_ZIP)
    
    # Extract the ZIP file
    print(f"Extracting match data to {MATCHES_DIR}")
    with zipfile.ZipFile(TEMP_ZIP, "r") as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith(".json"):
                # Extract only JSON files directly to matches directory
                match_id = os.path.basename(file)
                with zip_ref.open(file) as source, open(MATCHES_DIR / match_id, "wb") as target:
                    shutil.copyfileobj(source, target)
    
    # Remove the temporary ZIP file
    TEMP_ZIP.unlink()
    print("Extracted all match data")

def download_people():
    """Download people data."""
    download_file(PEOPLE_URL, PEOPLE_CSV)

def main():
    """Main function to download all data."""
    print("Starting data download...")
    ensure_directories()
    download_people()
    download_and_extract_matches()
    print("Data download completed successfully!")

if __name__ == "__main__":
    main()
