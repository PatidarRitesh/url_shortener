import csv
import os
from datetime import datetime, timedelta

CSV_FILE = "url_mapping.csv"
EXPIRY_DAYS = 7

# ✅ Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["short_url", "long_url", "click_count", "expiry_date"])  # Header row

def read_url_mapping():
    """Reads URL mappings from CSV and returns a dictionary."""
    url_mapping = {}

    if not os.path.exists(CSV_FILE):
        return url_mapping

    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) == 4:
                short_url, long_url, click_count, expiry_date = row
                url_mapping[short_url] = {
                    "long_url": long_url,
                    "click_count": int(click_count),
                    "expiry_date": expiry_date
                }
    return url_mapping

def write_url_mapping(short_url, long_url):
    """Writes a new URL mapping to CSV with an expiry date."""
    expiry_date = (datetime.utcnow() + timedelta(days=EXPIRY_DAYS)).strftime('%Y-%m-%d %H:%M:%S')
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([short_url, long_url, 0, expiry_date])

def update_click_count(short_url, url_mapping):
    """Updates the CSV file with the incremented click count."""
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["short_url", "long_url", "click_count", "expiry_date"])  # Header
        for s_url, data in url_mapping.items():
            writer.writerow([s_url, data["long_url"], data["click_count"], data["expiry_date"]])
