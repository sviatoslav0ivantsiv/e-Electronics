from models import Product, User, UserRegister, UserLogin
from typing import List
from fastapi import FastAPI, HTTPException, Query, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.7:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# ------------------- ROUTES -------------------

def require_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        if not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="Admins only")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/products")
def get_products(
    category: str | None = Query(None),
    brand: List[str] | None = Query(None),
    model: List[str] | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    min_display_size: float | None = Query(None),
    max_display_size: float | None = Query(None),
    min_battery_capacity: int | None = Query(None),
    max_battery_capacity: int | None = Query(None),
    camera: List[int] | None = Query(None),
    cpu: List[str] | None = Query(None),
    gpu: List[str] | None = Query(None),
    min_screen_size: float | None = Query(None),
    max_screen_size: float | None = Query(None),
    min_weight: float | None = Query(None),
    max_weight: float | None = Query(None),
    screen_type: List[str] | None = Query(None),
    min_battery_life: int | None = Query(None),
    max_battery_life: int | None = Query(None),
    water_resistance: List[str] | None = Query(None),
    ram: List[int] | None = Query(None),
    storage: List[int] | None = Query(None),
    sort: str = Query("desc"),
    page: int = Query(1),
    limit: int = Query(10)
    ):

    try:
        return Product.get_products(category, brand, min_price, max_price, model, min_display_size, max_display_size,
                                    min_battery_capacity, max_battery_capacity, camera, cpu, gpu, min_screen_size, max_screen_size,
                                    min_weight, max_weight, screen_type, min_battery_life, max_battery_life, water_resistance,
                                    ram, storage,
                                    sort,
                                    page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/products")
def create_product(data: dict = Body(...), admin=Depends(require_admin)):
    try:
        Product.save(data)
        return {"message": "Product created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/products/{product_id}")
def update_product(product_id: int, data: dict = Body(...), admin=Depends(require_admin)):
    try:
        return Product.update(product_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/api/products/{product_id}")
def patch_product(product_id: int, data: dict = Body(...), admin=Depends(require_admin)):
    try:
        return Product.patch(product_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, admin=Depends(require_admin)):
    try:
        return Product.delete(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    # ===filters===

@app.get("/api/filters")
def get_filters(category: str | None = Query(None)):
    try:
        return Product.get_filter_options(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # ===user===

@app.post("/auth/register")
def register_user(user: UserRegister):
    try:
        return User.register(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/login")
def login_user(user: UserLogin):
    try:
        return User.login(user.name, user.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/admin/users")
def get_users(admin=Depends(require_admin)):
    try:
        return User.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.patch("api/admin/users/{id}/toggle-admin")
def toggle_admin(user_id: int, admin=Depends(require_admin)):
    try:
        return User.toggle_admin(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))