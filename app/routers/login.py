from fastapi import APIRouter, HTTPException
from auth import verify_password, create_access_token
from model import LoginRequest
from database import cursor
router = APIRouter()

@router.post("/login")
def login(user: LoginRequest):
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (user.username,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credential"
        )
    
    valid = verify_password(user.password, row[0])

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid credential"
        )

    token = create_access_token(user.username)    

    return {
        "access_token": token
    }
