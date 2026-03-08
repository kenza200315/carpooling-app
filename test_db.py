#!/usr/bin/env python
from database import SessionLocal
from models import Trip

# Get a database session
db = SessionLocal()

try:
    # Query all trips
    trips = db.query(Trip).all()
    print(f"Found {len(trips)} trips")
    for trip in trips:
        print(f"  Trip {trip.id}: {trip.departure_city} -> {trip.destination_city}")
finally:
    db.close()
