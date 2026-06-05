from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from database import cursor
import jwt
import bcrypt

SECRET_KEY = "reallysecret"
bearer_scheme = HTTPBearer()

def password_hash(password):
    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    return hashed

def verify_password(password, stored_hash):    
    verified = bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    )

    if not verified:
        raise HTTPException(
            status_code=401,
            detail="Invalid credential"
        )

def create_acess_token(username):
    payload = jwt.encode(
        {"username": username},
        SECRET_KEY,
        algorithm="HS256"
    )

    return payload

def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=401,
            detail="invalid credential"
        )
    
    return payload["username"]

def get_user_id(username):
    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    user_id = row[0]
    return user_id




    

