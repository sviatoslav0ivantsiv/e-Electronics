from fastapi import APIRouter, HTTPException, Depends
from . import service
from src.users.model import UserCredentials
from src.auth.controller import require_admin

router = APIRouter(prefix="/api", tags=["Users"])

@router.post("/auth/register")
def register_user(user: UserCredentials):
    try:
        return service.register(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/users")
def get_users(admin=Depends(require_admin)):
    try:
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/admin/users/{user_id}/toggle-admin")
def toggle_admin(user_id: int, admin=Depends(require_admin)):
    try:
        return service.toggle_admin(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))