from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Trip
from schemas import Trip as TripSchema, TripBase, TripSearch, TripCreate, TripResponse, TripCreateResponse

router = APIRouter(prefix="/trips", tags=["trips"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_trips(db: Session = Depends(get_db)):
    """Get all trips"""
    trips = db.query(Trip).all()
    result = []
    for trip in trips:
        trip_dict = {
            "id": trip.id,
            "driver_id": trip.driver_id,
            "departure_city": trip.departure_city,
            "destination_city": trip.destination_city,
            "price": trip.price,
            "available_seats": trip.available_seats
        }
        # Try to get driver name, but if it fails, use Unknown
        try:
            if trip.driver:
                trip_dict["driver_name"] = trip.driver.name
            else:
                trip_dict["driver_name"] = "Unknown"
        except:
            trip_dict["driver_name"] = "Unknown"
        
        result.append(trip_dict)
    return result

@router.get("/search", response_model=list[TripSchema])
def search_trips(
    departure_city: str = None,
    destination_city: str = None,
    max_price: float = None,
    min_price: float = None,
    db: Session = Depends(get_db)
):
    query = db.query(Trip)
    if departure_city:
        query = query.filter(Trip.departure_city.ilike(f"%{departure_city}%"))
    if destination_city:
        query = query.filter(Trip.destination_city.ilike(f"%{destination_city}%"))
    if min_price is not None:
        query = query.filter(Trip.price >= min_price)
    if max_price is not None:
        query = query.filter(Trip.price <= max_price)
    return query.all()

@router.post("/")
def create_trip(trip: TripBase, db: Session = Depends(get_db)):
    """Create a new trip"""
    try:
        # Create trip object with base fields
        db_trip = Trip(
            driver_id=trip.driver_id,
            departure_city=trip.departure_city,
            destination_city=trip.destination_city,
            price=trip.price,
            available_seats=trip.available_seats
        )
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        return {
            "id": db_trip.id,
            "driver_id": db_trip.driver_id,
            "departure_city": db_trip.departure_city,
            "destination_city": db_trip.destination_city,
            "price": db_trip.price,
            "available_seats": db_trip.available_seats
        }
    except Exception as e:
        print(f"Error creating trip: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error creating trip: {str(e)}")

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return {"message": "Trip deleted"}