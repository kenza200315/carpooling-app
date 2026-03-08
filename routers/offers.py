from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Offer
from schemas import Offer as OfferSchema, OfferCreate, OfferUpdate
from pydantic import BaseModel

router = APIRouter(prefix="/offers", tags=["offers"])

class CounterOfferRequest(BaseModel):
    counter_price_da: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OfferSchema)
def create_offer(offer: OfferCreate, db: Session = Depends(get_db)):
    """Create a new offer"""
    db_offer = Offer(**offer.dict(), status="pending")
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

@router.get("/trip/{trip_id}", response_model=list[OfferSchema])
def get_trip_offers(trip_id: int, db: Session = Depends(get_db)):
    """Get all offers for a trip"""
    offers = db.query(Offer).filter(Offer.trip_id == trip_id).order_by(Offer.created_at.desc()).all()
    return offers

@router.get("/{offer_id}", response_model=OfferSchema)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    """Get a specific offer"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.put("/{offer_id}/accept", response_model=OfferSchema)
def accept_offer(offer_id: int, db: Session = Depends(get_db)):
    """Accept an offer"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    offer.status = "accepted"
    db.commit()
    db.refresh(offer)
    return offer

@router.put("/{offer_id}/reject", response_model=OfferSchema)
def reject_offer(offer_id: int, db: Session = Depends(get_db)):
    """Reject an offer"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    
    offer.status = "rejected"
    db.commit()
    db.refresh(offer)
    return offer

@router.put("/{offer_id}/counter", response_model=OfferSchema)
def counter_offer(offer_id: int, request: CounterOfferRequest, db: Session = Depends(get_db)):
    """Counter an offer with a new price"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    offer.counter_price = request.counter_price_da
    offer.status = "counter_offer"
    db.commit()
    db.refresh(offer)
    return offer

@router.patch("/{offer_id}", response_model=OfferSchema)
def update_offer(offer_id: int, offer_update: OfferUpdate, db: Session = Depends(get_db)):
    """Update an offer"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    for key, value in offer_update.dict(exclude_unset=True).items():
        setattr(offer, key, value)

    db.commit()
    db.refresh(offer)
    return offer

@router.delete("/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    """Delete an offer"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    db.delete(offer)
    db.commit()
    return {"message": "Offer deleted successfully"}