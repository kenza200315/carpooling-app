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
    try:
        trips = db.query(Trip).filter(Trip.status == "active").all()
        result = []
        for trip in trips:
            trip_dict = {
                "id": trip.id,
                "driver_id": trip.driver_id,
                "departure_city": trip.departure_city,
                "destination_city": trip.destination_city,
                "departure_lat": trip.departure_lat,
                "departure_lng": trip.departure_lng,
                "destination_lat": trip.destination_lat,
                "destination_lng": trip.destination_lng,
                "price": trip.price,
                "available_seats": trip.available_seats,
                "description": getattr(trip, 'description', None),
                "status": getattr(trip, 'status', 'active'),
                "driver_name": "Unknown",
                "driver_photo": None,
                "driver_rating": 0.0,
                "total_reviews": 0
            }
            # Try to get driver name and profile
            try:
                if trip.driver:
                    trip_dict["driver_name"] = trip.driver.name
                    if trip.driver.driver_profile:
                        trip_dict["driver_photo"] = trip.driver.driver_profile.driver_photo
                        
                        # Get driver rating
                        from sqlalchemy import func
                        rating_result = db.query(func.avg(Review.rating).label('avg_rating')).filter(
                            Review.reviewee_id == trip.driver_id,
                            Review.review_type == "driver_review"
                        ).first()
                        if rating_result.avg_rating:
                            trip_dict["driver_rating"] = round(float(rating_result.avg_rating), 1)
                        
                        # Get total reviews
                        trip_dict["total_reviews"] = db.query(Review).filter(
                            Review.reviewee_id == trip.driver_id,
                            Review.review_type == "driver_review"
                        ).count()
                        
            except Exception as d_err:
                pass

            result.append(trip_dict)
        return result
    except Exception as e:
        import traceback
        print(f"Error getting trips: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching trips: {str(e)}")

@router.get("/search", response_model=list[TripSchema])
def search_trips(
    departure_city: str = None,
    destination_city: str = None,
    max_price: float = None,
    min_price: float = None,
    db: Session = Depends(get_db)
):
    """Search trips with filters"""
    query = db.query(Trip).filter(Trip.status == "active")
    if departure_city:
        query = query.filter(Trip.departure_city.ilike(f"%{departure_city}%"))
    if destination_city:
        query = query.filter(Trip.destination_city.ilike(f"%{destination_city}%"))
    if min_price is not None:
        query = query.filter(Trip.price >= min_price)
    if max_price is not None:
        query = query.filter(Trip.price <= max_price)
    return query.all()

@router.post("/", response_model=TripCreateResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    """Create a new trip"""
    try:
        # Create trip object with all fields
        db_trip = Trip(
            driver_id=trip.driver_id,
            departure_city=trip.departure_city,
            destination_city=trip.destination_city,
            price=trip.price,
            available_seats=trip.available_seats,
            description=trip.description,
            status="active"
        )
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        return TripCreateResponse(
            id=db_trip.id,
            driver_id=db_trip.driver_id,
            departure_city=db_trip.departure_city,
            destination_city=db_trip.destination_city,
            price=db_trip.price,
            available_seats=db_trip.available_seats,
            departure_lat=getattr(db_trip, 'departure_lat', None),
            departure_lng=getattr(db_trip, 'departure_lng', None),
            destination_lat=getattr(db_trip, 'destination_lat', None),
            destination_lng=getattr(db_trip, 'destination_lng', None),
            created_at=db_trip.created_at
        )
    except Exception as e:
        print(f"Error creating trip: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error creating trip: {str(e)}")

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """Get a specific trip"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return TripResponse(
        id=trip.id,
        driver_id=trip.driver_id,
        departure_city=trip.departure_city,
        destination_city=trip.destination_city,
        price=trip.price,
        available_seats=trip.available_seats,
        created_at=trip.created_at.isoformat(),
        driver_name=trip.driver.name if trip.driver else "Unknown"
    )

@router.put("/{trip_id}", response_model=TripSchema)
def update_trip(trip_id: int, trip_update: TripCreate, db: Session = Depends(get_db)):
    """Update a trip"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    for key, value in trip_update.dict(exclude_unset=True).items():
        setattr(trip, key, value)

    db.commit()
    db.refresh(trip)
    return trip

@router.put("/{trip_id}/cancel")
def cancel_trip(trip_id: int, db: Session = Depends(get_db)):
    """Cancel a trip"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    trip.status = "cancelled"
    db.commit()
    return {"message": "Trip cancelled successfully", "trip_id": trip_id}

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """Delete a trip"""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip.status = "cancelled"
    db.commit()
    return {"message": "Trip cancelled successfully"}

@router.get("/user/{user_id}/history")
def get_user_trip_history(user_id: int, db: Session = Depends(get_db)):
    """Get trip history for a user (as driver or passenger)"""
    # Get trips where user is driver
    driver_trips = db.query(Trip).filter(Trip.driver_id == user_id).all()
    
    result = []
    for trip in driver_trips:
        trip_dict = {
            "id": trip.id,
            "driver_id": trip.driver_id,
            "departure_city": trip.departure_city,
            "destination_city": trip.destination_city,
            "price": trip.price,
            "available_seats": trip.available_seats,
            "status": trip.status,
            "created_at": trip.created_at.isoformat()
        }
        result.append(trip_dict)
    
    return result