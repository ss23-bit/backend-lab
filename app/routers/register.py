from fastapi import APIRouter, HTTPException
from model import User
from database import conn, cursor
from auth import password_hash
from psycopg.errors import UniqueViolation


router = APIRouter()

@router.post("/register")
def register(user: User):
    
    hashed_password = password_hash(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (user.username, hashed_password)
        )
        conn.commit()
    
    except UniqueViolation:
        conn.rollback()

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    
    return {
        "status": "Registered"
    }
    
    


