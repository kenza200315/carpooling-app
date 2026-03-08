from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str = "passenger"

class User(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[User] = None

class TripBase(BaseModel):
    driver_id: int
    departure_city: str
    destination_city: str
    price: float
    available_seats: int

class TripCreateResponse(BaseModel):
    id: int
    driver_id: int
    departure_city: str
    destination_city: str
    price: float
    available_seats: int
    created_at: datetime
    class Config:
        from_attributes = True

class TripCreate(BaseModel):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class TripResponse(BaseModel):
    id: int
    driver_id: int
    departure_city: str
    destination_city: str
    price: float
    available_seats: int
    created_at: str
    driver_name: str
    class Config:
        from_attributes = True

class Trip(TripBase):
    id: int
    created_at: datetime
    driver_name: str
    class Config:
        from_attributes = True

class OfferBase(BaseModel):
    trip_id: int
    passenger_name: str
    proposed_price: float

class Offer(OfferBase):
    id: int
    status: str
    counter_price: Optional[float] = None
    created_at: datetime
    class Config:
        from_attributes = True

class OfferUpdate(BaseModel):
    status: str
    counter_price: Optional[float] = None

class PaymentBase(BaseModel):
    trip_id: int
    passenger_id: int
    amount: float
    payment_method: str

class Payment(PaymentBase):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    trip_id: int
    passenger_id: int
    seats_reserved: int

class Reservation(ReservationBase):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    trip_id: int
    reviewer_id: int
    rating: int
    comment: str

class Review(ReviewBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    user_id: int
    message: str

class Notification(NotificationBase):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class TripSearch(BaseModel):
    departure_city: Optional[str] = None
    destination_city: Optional[str] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None

class AdminStats(BaseModel):
    total_users: int
    total_trips: int
    total_reservations: int
    total_revenue: float