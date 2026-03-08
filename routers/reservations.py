from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Reservation
from schemas import Reservation as ReservationSchema, ReservationBase

router = APIRouter(prefix="/reservations", tags=["reservations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReservationSchema)
def create_reservation(reservation: ReservationBase, db: Session = Depends(get_db)):
    db_reservation = Reservation(**reservation.dict(), status="pending")
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get("/{trip_id}", response_model=list[ReservationSchema])
def get_reservations(trip_id: int, db: Session = Depends(get_db)):
    return db.query(Reservation).filter(Reservation.trip_id == trip_id).all()