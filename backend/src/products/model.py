from pydantic import BaseModel
from typing import Optional, List

class ProductCreate(BaseModel):
    category: str
    brand: str
    model: str
    price: float
    stock: int = 0
    description: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    camera_mp: Optional[int] = None
    screen_size: Optional[float] = None
    battery_capacity: Optional[int] = None
    screen_type: Optional[str] = None

class ProductFilterParams(BaseModel):
    category: Optional[str] = None
    brand: Optional[List[str]] = None
    model: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_display_size: Optional[float] = None
    max_display_size: Optional[float] = None
    min_battery_capacity: Optional[int] = None
    max_battery_capacity: Optional[int] = None
    camera: Optional[List[int]] = None
    cpu: Optional[List[str]] = None
    gpu: Optional[List[str]] = None
    min_screen_size: Optional[float] = None
    max_screen_size: Optional[float] = None
    min_weight: Optional[float] = None
    max_weight: Optional[float] = None
    screen_type: Optional[List[str]] = None
    min_battery_life: Optional[int] = None
    max_battery_life: Optional[int] = None
    water_resistance: Optional[List[str]] = None
    ram: Optional[List[int]] = None
    storage: Optional[List[int]] = None
    
    sort: str = "desc"
    page: int = 1
    limit: int = 10