from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from . import service
from src.users.model import UserCredentials
from src.rate_limiting import limiter


router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()

def require_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        secret = os.getenv("SECRET_KEY")
        algo = os.getenv("ALGORITHM", "HS256")
        payload = jwt.decode(credentials.credentials, secret, algorithms=[algo])
        if not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="Admins only")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login")
@limiter.limit("5/minute")
def login(user: UserCredentials):
    try:
        token = service.login(user.name, user.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "message": "Login successful",
            "token": token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))