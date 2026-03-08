from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Offer
from schemas import Offer as OfferSchema, OfferBase, OfferUpdate

router = APIRouter(prefix="/offers", tags=["offers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OfferSchema)
def create_offer(offer: OfferBase, db: Session = Depends(get_db)):
    db_offer = Offer(**offer.dict(), status="pending")
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

@router.get("/{trip_id}", response_model=list[OfferSchema])
def get_offers(trip_id: int, db: Session = Depends(get_db)):
    return db.query(Offer).filter(Offer.trip_id == trip_id).all()

@router.patch("/{offer_id}", response_model=OfferSchema)
def update_offer(offer_id: int, offer_update: OfferUpdate, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    for key, value in offer_update.dict().items():
        setattr(offer, key, value)
    db.commit()
    db.refresh(offer)
    return offer

@router.patch("/{offer_id}/counter", response_model=OfferSchema)
def counter_offer(offer_id: int, counter_price: float, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    offer.counter_price = counter_price
    db.commit()
    db.refresh(offer)
    return offer