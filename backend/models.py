from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    long_url: HttpUrl  # Ensures only valid URLs are accepted

class URLResponse(BaseModel):
    short_url: str
