from fastapi import FastAPI, HTTPException, Query, Request
from models import Product
from fastapi.middleware.cors import CORSMiddleware
# from .db import get_connection

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

# @app.get("/api/products")
# def get_products(category: str | None = Query(None), page: int = Query(1), limit: int = Query(10)):
#     try:
#         if category:
#             return Product.by_category(category, page, limit)
#         else:
#             return Product.paginate(page, limit)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# def get_products(category=None, brand=None, min_price=None, max_price=None, model=None, ram=None, storage=None,
#                      min_display_size=None, max_display_size=None, min_battery_capacity=None, max_battery_capacity=None,
#                      cpu=None, gpu=None, min_screen_size=None, max_screen_size=None, min_weight=None, max_weight=None,
#                      screen_type=None, min_battery_life=None, max_battery_life=None, water_resistance=None,
#                      page=1, limit=10 ):

@app.get("/api/products")
def get_products(category: str | None = Query(None), brand: str | None = Query(None),
                min_price: float | None = Query(None), max_price: float | None = Query(None),
                model: str | None = Query(None),
                min_display_size: float | None = Query(None), max_display_size: float | None = Query(None),
                min_battery_capacity: int | None = Query(None), max_battery_capacity: int | None = Query(None),
                camera: int | None = Query(None), cpu: str | None = Query(None), gpu: str | None = Query(None),
                min_screen_size: float | None = Query(None), max_screen_size: float | None = Query(None),
                min_weight: float | None = Query(None), max_weight: float | None = Query(None),
                screen_type: str | None = Query(None),
                min_battery_life: int | None = Query(None), max_battery_life: int | None = Query(None),
                water_resistance: str | None = Query(None),
                ram: int | None = Query(None), storage: int | None = Query(None),
                page: int = Query(1), limit: int = Query(10)
                ):

    try:
        return Product.get_products(category, brand, min_price, max_price, model, min_display_size, max_display_size,
                                    min_battery_capacity, max_battery_capacity, camera, cpu, gpu, min_screen_size, max_screen_size,
                                    min_weight, max_weight, screen_type, min_battery_life, max_battery_life, water_resistance,
                                    ram, storage,
                                    page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filters")
def get_filters(category: str | None = Query(None)):
    try:
        return Product.get_filter_options(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


