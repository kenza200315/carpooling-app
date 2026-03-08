from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Review
from schemas import Review as ReviewSchema, ReviewCreate

router = APIRouter(prefix="/reviews", tags=["reviews"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReviewSchema)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review"""
    # Validate rating is between 1-5
    if not 1 <= review.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/trip/{trip_id}", response_model=list[ReviewSchema])
def get_trip_reviews(trip_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a trip"""
    reviews = db.query(Review).filter(Review.trip_id == trip_id).all()
    return reviews

@router.get("/user/{user_id}", response_model=list[ReviewSchema])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a user (as reviewee)"""
    reviews = db.query(Review).filter(Review.reviewee_id == user_id).all()
    return reviews

@router.get("/user/{user_id}/given", response_model=list[ReviewSchema])
def get_reviews_given(user_id: int, db: Session = Depends(get_db)):
    """Get all reviews given by a user"""
    reviews = db.query(Review).filter(Review.reviewer_id == user_id).all()
    return reviews

@router.get("/driver/{driver_id}/rating")
def get_driver_rating(driver_id: int, db: Session = Depends(get_db)):
    """Get average rating for a driver"""
    from sqlalchemy import func
    
    result = db.query(func.avg(Review.rating).label('average_rating')).filter(
        Review.reviewee_id == driver_id,
        Review.review_type == "driver_review"
    ).first()
    
    average_rating = float(result.average_rating) if result.average_rating else 0.0
    
    # Get total reviews count
    total_reviews = db.query(Review).filter(
        Review.reviewee_id == driver_id,
        Review.review_type == "driver_review"
    ).count()
    
    return {
        "driver_id": driver_id,
        "average_rating": round(average_rating, 1),
        "total_reviews": total_reviews
    }