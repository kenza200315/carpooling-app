from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="passenger")  # passenger, driver, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    trips = relationship("Trip", back_populates="driver")
    reservations = relationship("Reservation", back_populates="passenger")
    reviews_given = relationship("Review", foreign_keys="Review.reviewer_id", back_populates="reviewer")
    notifications = relationship("Notification", back_populates="user")
    driver_profile = relationship("DriverProfile", back_populates="user", uselist=False)
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")

class DriverProfile(Base):
    __tablename__ = "driver_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    phone_number = Column(String)
    car_brand = Column(String)
    car_color = Column(String)
    car_plate_number = Column(String)
    identity_card_photo = Column(String)  # File path or URL
    driver_photo = Column(String, nullable=True)  # Driver profile photo
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="driver_profile")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    departure_city = Column(String)
    destination_city = Column(String)
    departure_lat = Column(Float, nullable=True)
    departure_lng = Column(Float, nullable=True)
    destination_lat = Column(Float, nullable=True)
    destination_lng = Column(Float, nullable=True)
    price = Column(Float)
    available_seats = Column(Integer)
    description = Column(Text, nullable=True)
    status = Column(String, default="active")  # active, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    driver = relationship("User", back_populates="trips")
    offers = relationship("Offer", back_populates="trip")
    reservations = relationship("Reservation", back_populates="trip")
    payments = relationship("Payment", back_populates="trip")
    reviews = relationship("Review", back_populates="trip")
    messages = relationship("Message", back_populates="trip")

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    passenger_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    passenger_name = Column(String)
    passenger_phone = Column(String, nullable=True)
    proposed_price = Column(Float)
    status = Column(String, default="pending")  # pending, accepted, rejected, countered
    counter_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    trip = relationship("Trip", back_populates="offers")
    passenger = relationship("User", foreign_keys=[passenger_id])

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    passenger_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    payment_method = Column(String, default="cash")  # cash, card
    payment_status = Column(String, default="pending")  # pending, completed, failed, refunded
    transaction_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    trip = relationship("Trip", back_populates="payments")
    passenger = relationship("User", foreign_keys=[passenger_id])

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    trip = relationship("Trip", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))  # Person giving the review
    reviewee_id = Column(Integer, ForeignKey("users.id"))  # Person being reviewed
    rating = Column(Integer)  # 1-5 stars
    comment = Column(Text, nullable=True)
    review_type = Column(String)  # driver_review, passenger_review
    created_at = Column(DateTime, default=datetime.utcnow)
    trip = relationship("Trip", back_populates="reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewee = relationship("User", foreign_keys=[reviewee_id])

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(Text)
    type = Column(String)  # offer_received, trip_cancelled, payment_received, etc.
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="notifications")

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    passenger_id = Column(Integer, ForeignKey("users.id"))
    seats_reserved = Column(Integer)
    status = Column(String, default="pending")  # pending, confirmed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    trip = relationship("Trip", back_populates="reservations")
    passenger = relationship("User", back_populates="reservations")