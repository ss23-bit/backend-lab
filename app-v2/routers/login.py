from fastapi import APIRouter, HTTPException
from auth import verify_password, create_acess_token
from model import User
from database import cursor

router = APIRouter()


@router.get("/login")
def login(user: User):
    cursor.execute(
        "SELECT username, password FROM users WHERE username, password = ?, ?",
        (user.username, user.password)
    )

    usr_pw = cursor.fetchone()

    if usr_pw is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credential"
        )
    
    verify_password(user.password, usr_pw[1])

    token = create_acess_token(user.username)

    return {
        "status": "login success",
        "access_token": token 
    }
