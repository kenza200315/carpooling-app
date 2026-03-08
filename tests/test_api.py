import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from database import SessionLocal

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "driver"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"

def test_login_user():
    response = client.post(
        "/auth/login",
        json={
            "email": "john@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_trip():
    response = client.post(
        "/trips",
        json={
            "driver_id": 1,
            "departure_city": "New York",
            "destination_city": "Boston",
            "price": 25.50,
            "available_seats": 4
        }
    )
    assert response.status_code == 200
    assert response.json()["departure_city"] == "New York"

def test_get_trips():
    response = client.get("/trips")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_trips():
    response = client.get(
        "/trips/search?departure_city=New+York&max_price=30"
    )
    assert response.status_code == 200

def test_create_offer():
    response = client.post(
        "/offers",
        json={
            "trip_id": 1,
            "passenger_name": "Jane Doe",
            "proposed_price": 20.00
        }
    )
    assert response.status_code == 200

def test_create_payment():
    response = client.post(
        "/payments",
        json={
            "trip_id": 1,
            "passenger_id": 1,
            "amount": 25.50,
            "payment_method": "credit_card"
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"

def test_create_reservation():
    response = client.post(
        "/reservations",
        json={
            "trip_id": 1,
            "passenger_id": 1,
            "seats_reserved": 2
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"

def test_create_review():
    response = client.post(
        "/reviews",
        json={
            "trip_id": 1,
            "reviewer_id": 1,
            "rating": 5,
            "comment": "Great driver!"
        }
    )
    assert response.status_code == 200

def test_invalid_rating():
    response = client.post(
        "/reviews",
        json={
            "trip_id": 1,
            "reviewer_id": 1,
            "rating": 10,
            "comment": "Invalid rating"
        }
    )
    assert response.status_code == 400