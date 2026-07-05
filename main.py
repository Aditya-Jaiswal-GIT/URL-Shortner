# app.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from schemas import URLCreate
from crud import (
    create_short_url,
    get_url,
    increment_click,
    delete_url,
    get_all_urls
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="URL Shortener API",
    description="Simple URL Shortener using FastAPI & SQLite",
    version="1.0.0"
)

# Dependency to get DB session
def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Home Route
@app.get("/")
def home():

    return {
        "message": "Welcome to URL Shortener API 🚀"
    }


# Create Short URL
@app.post("/shorten")
def shorten_url(
    data: URLCreate,
    db: Session = Depends(get_db)
):

    url = create_short_url(
        db,
        data.original_url
    )

    return {
        "original_url": url.original_url,
        "short_url": f"http://127.0.0.1:8000/{url.short_code}"
    }


# Redirect to Original URL
@app.get("/{code}")
def redirect_url(
    code: str,
    db: Session = Depends(get_db)
):

    url = get_url(db, code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    increment_click(db, url)

    return RedirectResponse(
        url=url.original_url
    )


# URL Analytics
@app.get("/stats/{code}")
def url_stats(
    code: str,
    db: Session = Depends(get_db)
):

    url = get_url(db, code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks
    }


# Delete URL
@app.delete("/delete/{code}")
def remove_url(
    code: str,
    db: Session = Depends(get_db)
):

    url = delete_url(db, code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    return {
        "message": "URL deleted successfully"
    }


# Get All URLs
@app.get("/urls")
def all_urls(
    db: Session = Depends(get_db)
):

    return get_all_urls(db)