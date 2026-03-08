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

class DriverProfileBase(BaseModel):
    user_id: int
    phone_number: str
    car_brand: str
    car_color: str
    car_plate_number: str
    identity_card_photo: str
    driver_photo: Optional[str] = None

class DriverProfileCreate(DriverProfileBase):
    pass

class DriverProfile(DriverProfileBase):
    id: int
    is_verified: bool
    created_at: datetime
    class Config:
        from_attributes = True

class TripBase(BaseModel):
    driver_id: int
    departure_city: str
    destination_city: str
    price: float
    available_seats: int
    departure_lat: Optional[float] = None
    departure_lng: Optional[float] = None
    destination_lat: Optional[float] = None
    destination_lng: Optional[float] = None

class TripCreate(TripBase):
    description: Optional[str] = None

class TripCreateResponse(BaseModel):
    id: int
    driver_id: int
    departure_city: str
    destination_city: str
    price: float
    available_seats: int
    departure_lat: Optional[float] = None
    departure_lng: Optional[float] = None
    destination_lat: Optional[float] = None
    destination_lng: Optional[float] = None
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
    departure_lat: Optional[float]
    departure_lng: Optional[float]
    destination_lat: Optional[float]
    destination_lng: Optional[float]
    created_at: str
    driver_name: str
    class Config:
        from_attributes = True

class Trip(TripBase):
    id: int
    description: Optional[str]
    status: str
    created_at: datetime
    driver_name: str
    class Config:
        from_attributes = True

class OfferBase(BaseModel):
    trip_id: int
    passenger_name: str
    proposed_price: float

class OfferCreate(OfferBase):
    passenger_id: Optional[int] = None
    passenger_phone: Optional[str] = None

class Offer(OfferBase):
    id: int
    passenger_id: Optional[int]
    passenger_phone: Optional[str]
    status: str
    counter_price: Optional[float]
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class OfferUpdate(BaseModel):
    status: str
    counter_price: Optional[float] = None

class ReservationBase(BaseModel):
    trip_id: int
    passenger_id: int
    seats_booked: int = 1

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    trip_id: int
    passenger_id: int
    amount: float
    payment_method: str = "cash"

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    payment_status: str
    transaction_id: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    trip_id: int
    sender_id: int
    receiver_id: int
    message: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    trip_id: int
    reviewer_id: int
    reviewee_id: int
    rating: int
    comment: Optional[str] = None
    review_type: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    type: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    is_read: bool
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