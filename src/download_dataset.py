"""download_dataset.py

Utility script to download the public Superstore Sales CSV into the project’s ``data/raw`` folder.

If you have a Kaggle API token you can also use the kaggle CLI (instructions are in the README),
but this script works without credentials by pulling the file from a publicly‑hosted GitHub URL.
"""

import pathlib
import urllib.request
import shutil

# Resolve project root (two levels up from this file)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Public raw URL of the Superstore CSV (spaces URL‑encoded)
URL = (
    "https://raw.githubusercontent.com/yajasarora/Superstore-Sales-Analysis-with-Tableau/master/"
    "Superstore%20sales%20dataset.csv"
)
DEST = RAW_DATA_DIR / "Superstore.csv"

def download():
    if DEST.is_file():
        print(f"✅ {DEST.name} already exists – skipping download.")
        return
    print(f"Downloading Superstore dataset from {URL} ...")
    with urllib.request.urlopen(URL) as response, open(DEST, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
    print(f"✅ Download complete. Saved to {DEST}")

if __name__ == "__main__":
    download()
