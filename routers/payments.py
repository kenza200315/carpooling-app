from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Payment
from schemas import Payment as PaymentSchema, PaymentBase

router = APIRouter(prefix="/payments", tags=["payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PaymentSchema)
def create_payment(payment: PaymentBase, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict(), status="pending")
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/{trip_id}", response_model=list[PaymentSchema])
def get_payments(trip_id: int, db: Session = Depends(get_db)):
    return db.query(Payment).filter(Payment.trip_id == trip_id).all()