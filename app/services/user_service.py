from models.user import User
from database import SessionLocal
from fastapi import HTTPException

def create_user(username: str, password: str):
    db = SessionLocal()
    
    try:
        user = User(
            username=username,
            password=password
        )

        db.add(user)
        db.commit()
    
    finally:
        db.close()

def get_user(username: str):
    db = SessionLocal()
    
    try:
        user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user

    finally:    
        db.close()

    