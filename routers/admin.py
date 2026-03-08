from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
from models import User, Trip, Reservation, Payment
from schemas import User as UserSchema, AdminStats

router = APIRouter(prefix="/admin", tags=["admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=list[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/stats", response_model=AdminStats)
def get_stats(db: Session = Depends(get_db)):
    total_users = db.query(func.count(User.id)).scalar()
    total_trips = db.query(func.count(Trip.id)).scalar()
    total_reservations = db.query(func.count(Reservation.id)).scalar()
    total_revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.status == "paid"
    ).scalar() or 0
    
    return {
        "total_users": total_users or 0,
        "total_trips": total_trips or 0,
        "total_reservations": total_reservations or 0,
        "total_revenue": float(total_revenue)
    }

@router.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted"}