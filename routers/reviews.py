from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Review
from schemas import Review as ReviewSchema, ReviewBase

router = APIRouter(prefix="/reviews", tags=["reviews"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReviewSchema)
def create_review(review: ReviewBase, db: Session = Depends(get_db)):
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/{trip_id}", response_model=list[ReviewSchema])
def get_reviews(trip_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.trip_id == trip_id).all()