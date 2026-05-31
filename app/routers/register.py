from fastapi import APIRouter, status, HTTPException
from auth import hash_password
from model import LoginRequest
from database import conn, cursor
import sqlite3

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: LoginRequest):
    
    hashed_password = hash_password(user.password)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hashed_password)
        )
    
        conn.commit()
    
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return {
        "status": "created"
    }

    


