from fastapi import APIRouter, HTTPException
from services.user_service import create_user
from schemas import UserCreate
from auth import password_hash
from psycopg.errors import UniqueViolation


router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    
    hashed_password = password_hash(user.password)

    create_user(user.username, hashed_password)
    
    return {
        "status": "Registered"
    }
    
    


