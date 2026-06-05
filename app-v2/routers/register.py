from fastapi import APIRouter, HTTPException
from model import User
from database import conn, cursor
from auth import password_hash
import sqlite3

router = APIRouter()

@router.post("/register")
def register(user: User):
    
    hashed_password = password_hash(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hashed_password)
        )
        conn.commit
    
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    
    return {
        "status": "Registered"
    }
    
    


