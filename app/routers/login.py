from fastapi import APIRouter, HTTPException
from auth import verify_password, create_acess_token
from schemas import UserCreate
from services.user_service import get_user 

router = APIRouter()


@router.post("/login")
def login(user: UserCreate):

    stored_user = get_user(user.username)

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credential"
        )
    
    verify_password(user.password, stored_user.password)

    token = create_acess_token(stored_user.username)

    return {
        "status": "login success",
        "access_token": token 
    }
