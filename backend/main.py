from fastapi import FastAPI, HTTPException, Query
from models import Product, User, UserRegister, UserLogin
from fastapi.middleware.cors import CORSMiddleware
from typing import List


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/api/filters")
def get_filters(category: str | None = Query(None)):
    try:
        return Product.get_filter_options(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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