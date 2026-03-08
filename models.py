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

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    departure_city = Column(String)
    destination_city = Column(String)
    price = Column(Float)
    available_seats = Column(Integer)
    driver = relationship("User", back_populates="trips")
    offers = relationship("Offer", back_populates="trip")
    reservations = relationship("Reservation", back_populates="trip")
    payments = relationship("Payment", back_populates="trip")
    reviews = relationship("Review", back_populates="trip")

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    passenger_name = Column(String)
    proposed_price = Column(Float)
    status = Column(String)  # pending, accepted, rejected
    counter_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    trip = relationship("Trip", back_populates="offers")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    passenger_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    payment_method = Column(String)  # credit_card, paypal, stripe
    status = Column(String, default="pending")  # pending, paid, refunded
    created_at = Column(DateTime, default=datetime.utcnow)
    trip = relationship("Trip", back_populates="payments")

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

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)  # 1-5 stars
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    trip = relationship("Trip", back_populates="reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    status = Column(String, default="unread")  # unread, read
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="notifications")