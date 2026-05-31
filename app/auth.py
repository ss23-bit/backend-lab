from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
import jwt
import bcrypt

SECRET_KEY = "ordinarysecretkey"

bearer_scheme = HTTPBearer()

def hash_password(password):
    
    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    return hashed_password

def verify_password(password, stored_hash):
    
    return bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    )


def create_access_token(username):
    
    return jwt.encode(
        {"username": username},
        SECRET_KEY,
        algorithm="HS256"
    )



def verify_access_token(credential: HTTPAuthorizationCredentials = Depends(bearer_scheme)):

    token = credential.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    
        return payload
    
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
