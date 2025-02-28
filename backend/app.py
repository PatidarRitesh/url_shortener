# import csv
# import random
# import string
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import RedirectResponse
# from pydantic import BaseModel
# from pathlib import Path
# import uvicorn

# app = FastAPI()

# # Path to the CSV file
# CSV_FILE = "url_mapping.csv"

# # Ensure the CSV file exists
# Path(CSV_FILE).touch(exist_ok=True)

# # Pydantic models
# class URLRequest(BaseModel):
#     long_url: str

# class URLResponse(BaseModel):
#     short_url: str

# # Generate a random short URL
# def generate_short_url():
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# # Read URL mappings from CSV
# def read_url_mapping():
#     url_mapping = {}
#     with open(CSV_FILE, mode="r") as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if len(row) == 2:  # Ensure the row has both short_url and long_url
#                 short_url, long_url = row
#                 url_mapping[short_url] = long_url
#     return url_mapping

# # Write a single mapping to CSV
# def write_url_mapping(short_url, long_url):
#     with open(CSV_FILE, mode="a", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow([short_url, long_url])

# @app.post("/shorten", response_model=URLResponse)
# def create_short_url(request: URLRequest):
#     """Shorten a long URL."""
#     url_mapping = read_url_mapping()

#     # Check if the long URL already exists
#     for short_url, long_url in url_mapping.items():
#         if long_url == request.long_url:
#             return URLResponse(short_url=f"http://127.0.0.1:8000/{short_url}")

#     # Generate a unique short URL
#     short_url = generate_short_url()
#     while short_url in url_mapping:
#         short_url = generate_short_url()

#     # Save the mapping
#     write_url_mapping(short_url, request.long_url)
#     return URLResponse(short_url=f"http://127.0.0.1:8000/{short_url}")

# @app.get("/{short_url}")
# def redirect_to_long_url(short_url: str):
#     """Redirect to the original long URL."""
#     url_mapping = read_url_mapping()

#     long_url = url_mapping.get(short_url)
#     if not long_url:
#         raise HTTPException(status_code=404, detail="Short URL not found")

#     # Redirect to the original URL
#     return RedirectResponse(url=long_url)

# # This part will only be executed when the script is run directly
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)


import csv
import hashlib
import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify ["http://127.0.0.1:8001"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# CSV file path
CSV_FILE = "url_mapping.csv"

# Expiry configuration (URLs expire after 7 days)
EXPIRY_DAYS = 7

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["short_url", "long_url", "click_count", "expiry_date"])  # Add expiry column


# Pydantic model for request validation
class URLRequest(BaseModel):
    long_url: HttpUrl  # Ensures only valid URLs are accepted


class URLResponse(BaseModel):
    short_url: str


import hashlib

def generate_short_url(long_url):
    """Generate a short and unique identifier for the URL using MD5 hashing."""
    long_url_str = str(long_url)  # Convert HttpUrl to string
    return hashlib.md5(long_url_str.encode()).hexdigest()[:6]  # Use first 6 chars of the hash


def read_url_mapping():
    """Reads the URL mapping from the CSV file and handles an empty file gracefully."""
    url_mapping = {}

    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.reader(file)

        # Skip header if the file isn't empty
        try:
            header = next(reader)  # Skip the first row (header)
        except StopIteration:
            return url_mapping  # If file is empty, return an empty dictionary

        for row in reader:
            if len(row) == 4:  # Ensure correct number of columns
                short_url, long_url, click_count, expiry_date = row
                url_mapping[short_url] = {
                    "long_url": long_url,
                    "click_count": int(click_count),
                    "expiry_date": expiry_date
                }

    return url_mapping


# Write a single mapping to CSV
def write_url_mapping(short_url, long_url):
    """Writes a new URL mapping with an initial click count and expiration date."""
    expiry_date = (datetime.utcnow() + timedelta(days=EXPIRY_DAYS)).strftime('%Y-%m-%d %H:%M:%S')
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([short_url, long_url, 0, expiry_date])  # Initialize with 0 clicks


# Update click count in CSV
def update_click_count(short_url, url_mapping):
    """Updates the CSV file with the incremented click count."""
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["short_url", "long_url", "click_count", "expiry_date"])  # Write header
        for s_url, data in url_mapping.items():
            writer.writerow([s_url, data["long_url"], data["click_count"], data["expiry_date"]])


@app.post("/shorten", response_model=URLResponse)
def create_short_url(request: URLRequest):
    """Shorten a long URL and store it in the CSV file."""
    url_mapping = read_url_mapping()

    # Check if the long URL already exists in the mapping
    for short_url, data in url_mapping.items():
        if data["long_url"] == str(request.long_url):
            return URLResponse(short_url=f"http://127.0.0.1:8000/{short_url}")

    # Generate a unique short URL
    short_url = generate_short_url(request.long_url)
    while short_url in url_mapping:
        short_url = generate_short_url(request.long_url + str(len(url_mapping)))  # Avoid collision

    # Save the mapping
    write_url_mapping(short_url, str(request.long_url))
    return URLResponse(short_url=f"http://127.0.0.1:8000/{short_url}")


@app.get("/{short_url}")
def redirect_to_long_url(short_url: str):
    """Redirect to the original long URL and update click count."""
    url_mapping = read_url_mapping()

    if short_url not in url_mapping:
        raise HTTPException(status_code=404, detail="Short URL not found")

    long_url = url_mapping[short_url]["long_url"]
    expiry_date = url_mapping[short_url]["expiry_date"]

    # Check if URL is expired
    if datetime.utcnow() > datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S'):
        raise HTTPException(status_code=410, detail="Short URL has expired")

    # Increment click count
    url_mapping[short_url]["click_count"] += 1
    update_click_count(short_url, url_mapping)  # Save the updated count

    return RedirectResponse(url=long_url)


@app.get("/stats/{short_url}")
def get_url_stats(short_url: str):
    """Get statistics for a shortened URL (click count & expiration)."""
    url_mapping = read_url_mapping()

    if short_url not in url_mapping:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "long_url": url_mapping[short_url]["long_url"],
        "click_count": url_mapping[short_url]["click_count"],
        "expiry_date": url_mapping[short_url]["expiry_date"]
    }


# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
