from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from models import URLRequest, URLResponse
from database import read_url_mapping, write_url_mapping, update_click_count
from utils import generate_short_url
from datetime import datetime

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
def create_short_url(request: URLRequest):
    """Shortens a URL and saves it in the database."""
    url_mapping = read_url_mapping()

    # Check if the long URL already exists
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

@router.get("/{short_url}")
def redirect_to_long_url(short_url: str):
    """Redirects short URL to the original long URL and updates click count."""
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

@router.get("/stats/{short_url}")
def get_url_stats(short_url: str):
    """Retrieves statistics for a shortened URL (click count & expiration)."""
    url_mapping = read_url_mapping()

    if short_url not in url_mapping:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "long_url": url_mapping[short_url]["long_url"],
        "click_count": url_mapping[short_url]["click_count"],
        "expiry_date": url_mapping[short_url]["expiry_date"]
    }
