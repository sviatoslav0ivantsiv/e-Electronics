
from pydantic import BaseModel
from typing import Optional, List
from fastapi import Query

class ProductCreate(BaseModel):
    category: str
    brand: str
    model: str
    price: float
    stock: int = 0
    description: Optional[str] = None
    display_size: Optional[float] = None
    battery_capacity: Optional[int] = None
    camera_mp: Optional[int] = None
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    screen_size: Optional[float] = None
    weight: Optional[float] = None
    screen_type: Optional[str] = None
    battery_life: Optional[int] = None
    water_resistance: Optional[str] = None
    ram: Optional[int] = None      
    storage: Optional[int] = None

def product_filter_params(
    category: Optional[str] = Query(None),
    brand: Optional[List[str]] = Query(None, style="form", explode=True), 
    model: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_display_size: Optional[float] = Query(None),
    max_display_size: Optional[float] = Query(None),
    min_battery_capacity: Optional[int] = Query(None),
    max_battery_capacity: Optional[int] = Query(None),
    camera_mp: Optional[List[int]] = Query(None, style="form", explode=True),
    cpu: Optional[List[str]] = Query(None, style="form", explode=True),
    gpu: Optional[List[str]] = Query(None, style="form", explode=True),
    min_screen_size: Optional[float] = Query(None),
    max_screen_size: Optional[float] = Query(None),
    min_weight: Optional[float] = Query(None),
    max_weight: Optional[float] = Query(None),
    screen_type: Optional[List[str]] = Query(None, style="form", explode=True),
    min_battery_life: Optional[int] = Query(None),
    max_battery_life: Optional[int] = Query(None),
    water_resistance: Optional[List[str]] = Query(None, style="form", explode=True),
    ram: Optional[List[int]] = Query(None, style="form", explode=True),
    storage: Optional[List[int]] = Query(None, style="form", explode=True),
    sort: str = Query("desc"),
    page: int = Query(1),
    limit: int = Query(10),
) -> dict:
    return {
        "category": category,
        "brand": brand,
        "model": model,
        "min_price": min_price,
        "max_price": max_price,
        "min_display_size": min_display_size,
        "max_display_size": max_display_size,
        "min_battery_capacity": min_battery_capacity,
        "max_battery_capacity": max_battery_capacity,
        "camera_mp": camera_mp,
        "cpu": cpu,
        "gpu": gpu,
        "min_screen_size": min_screen_size,
        "max_screen_size": max_screen_size,
        "min_weight": min_weight,
        "max_weight": max_weight,
        "screen_type": screen_type,
        "min_battery_life": min_battery_life,
        "max_battery_life": max_battery_life,
        "water_resistance": water_resistance,
        "ram": ram,
        "storage": storage,
        "sort": sort,
        "page": page,
        "limit": limit,
    }