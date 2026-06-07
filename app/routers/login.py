from fastapi import APIRouter, HTTPException
from auth import verify_password, create_acess_token
from model import User
from database import cursor

router = APIRouter()


@router.post("/login")
def login(user: User):
    cursor.execute(
        "SELECT username, password FROM users WHERE username = %s",
        (user.username,)
    )

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credential"
        )
    
    verify_password(user.password, row[1])

    token = create_acess_token(user.username)

    return {
        "status": "login success",
        "access_token": token 
    }
