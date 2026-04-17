from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    category: str
    brand: str
    model: str
    price: float
    stock: int = 0 # Made mandatory, defaults to 0 if not provided
    description: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    camera_mp: Optional[int] = None
    screen_size: Optional[float] = None
    battery_capacity: Optional[int] = None
    screen_type: Optional[str] = None