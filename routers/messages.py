from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Message
from schemas import Message as MessageSchema, MessageCreate

router = APIRouter(prefix="/messages", tags=["messages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MessageSchema)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Create a new message"""
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/{trip_id}", response_model=list[MessageSchema])
def get_trip_messages(trip_id: int, db: Session = Depends(get_db)):
    """Get all messages for a trip"""
    messages = db.query(Message).filter(Message.trip_id == trip_id).order_by(Message.created_at).all()
    return messages

@router.get("/user/{user_id}", response_model=list[MessageSchema])
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    """Get all messages for a user (sent or received)"""
    messages = db.query(Message).filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).order_by(Message.created_at.desc()).all()
    return messages

@router.patch("/{message_id}/read")
def mark_message_read(message_id: int, db: Session = Depends(get_db)):
    """Mark a message as read"""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    message.is_read = True
    db.commit()
    return {"message": "Message marked as read"}