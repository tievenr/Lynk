import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from prometheus_client import Counter
from app.store import generate_code, set_url, get_url

router = APIRouter()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

urls_shortened = Counter("lynk_urls_shortened_total", "Total number of URLs shortened")
urls_redirected = Counter("lynk_urls_redirected_total", "Total number of redirects")
urls_not_found = Counter("lynk_urls_not_found_total", "Total number of 404s")

class ShortenRequest(BaseModel):
    url:str

@router.post("/shorten")
def shorten(request:ShortenRequest):
    code=generate_code()
    set_url(code,request.url)
    urls_shortened.inc()
    return {"short_code":code,"short_url":f"{BASE_URL}/{code}"}

@router.get("/health")
def health():
    return {"status": "healthy"}

@router.get("/{code}")
def redirect(code:str):
    url=get_url(code)
    if not url:
        urls_not_found.inc()
        raise HTTPException(status_code=404, detail="URL not found")
    urls_redirected.inc()
    return RedirectResponse(url=url)

