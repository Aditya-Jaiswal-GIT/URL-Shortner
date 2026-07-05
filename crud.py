# crud.py

from sqlalchemy.orm import Session
from models import URL
from utils import generate_code


# Create a new short URL
def create_short_url(db: Session, original_url: str):

    # Generate a unique short code
    code = generate_code()

    # Create URL object
    url = URL(
        original_url=original_url,
        short_code=code,
        clicks=0
    )

    # Save into database
    db.add(url)
    db.commit()
    db.refresh(url)

    return url


# Find URL using short code
def get_url(db: Session, code: str):

    return db.query(URL).filter(
        URL.short_code == code
    ).first()


# Increase click count
def increment_click(db: Session, url: URL):

    url.clicks += 1

    db.commit()


# Delete URL
def delete_url(db: Session, code: str):

    url = get_url(db, code)

    if url:
        db.delete(url)
        db.commit()

    return url


# Get all URLs
def get_all_urls(db: Session):

    return db.query(URL).all()