from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Notification
from schemas import Notification as NotificationSchema, NotificationBase

router = APIRouter(prefix="/notifications", tags=["notifications"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[NotificationSchema])
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).all()

@router.post("/", response_model=NotificationSchema)
def create_notification(notification: NotificationBase, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification