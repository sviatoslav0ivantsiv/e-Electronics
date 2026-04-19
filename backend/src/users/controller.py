from fastapi import APIRouter, HTTPException, Depends
from . import service
from src.users.model import UserCredentials
from src.auth.controller import require_admin
from src.rate_limiting import limiter
from fastapi import Request

router = APIRouter(prefix="/api", tags=["Users"])

@router.post("/auth/register")
@limiter.limit("5/minute")
def register_user(request: Request, user: UserCredentials):
    try:
        return service.register(user.name, user.password)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/admin/users")
@limiter.limit("5/minute")
def get_users(request: Request, admin=Depends(require_admin)):
    try:
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/admin/users/{user_id}/toggle-admin")
@limiter.limit("5/minute")
def toggle_admin(request: Request, user_id: int, admin=Depends(require_admin)):
    try:
        return service.toggle_admin(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))