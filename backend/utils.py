import hashlib

def generate_short_url(long_url):
    """Generate a short and unique identifier for the URL using MD5 hashing."""
    long_url_str = str(long_url)  # Convert HttpUrl to string
    return hashlib.md5(long_url_str.encode()).hexdigest()[:6]  # Use first 6 chars of the hash



