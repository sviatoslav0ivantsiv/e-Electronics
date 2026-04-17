from fastapi import APIRouter, HTTPException, Depends
from . import service
from src.users.model import UserRegister
from src.auth.controller import require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user: UserRegister):
    try:
        return service.register(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/all")
def get_users(admin=Depends(require_admin)):
    try:
        return service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/admin/{user_id}/toggle-admin")
def toggle_admin(user_id: int, admin=Depends(require_admin)):
    try:
        return service.toggle_admin(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))