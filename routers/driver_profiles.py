from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import DriverProfile
from schemas import DriverProfile as DriverProfileSchema, DriverProfileCreate

router = APIRouter(prefix="/driver-profiles", tags=["driver-profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DriverProfileSchema)
def create_driver_profile(profile: DriverProfileCreate, db: Session = Depends(get_db)):
    """Create a new driver profile"""
    # Check if user already has a profile
    existing_profile = db.query(DriverProfile).filter(DriverProfile.user_id == profile.user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Driver profile already exists for this user")

    db_profile = DriverProfile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/{user_id}", response_model=DriverProfileSchema)
def get_driver_profile(user_id: int, db: Session = Depends(get_db)):
    """Get driver profile by user ID"""
    profile = db.query(DriverProfile).filter(DriverProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Driver profile not found")
    return profile

@router.put("/{user_id}", response_model=DriverProfileSchema)
def update_driver_profile(user_id: int, profile_update: DriverProfileCreate, db: Session = Depends(get_db)):
    """Update driver profile"""
    profile = db.query(DriverProfile).filter(DriverProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Driver profile not found")

    for key, value in profile_update.dict().items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile