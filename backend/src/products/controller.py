from fastapi import APIRouter, HTTPException, Depends, Query, Request
from . import service
from src.auth.controller import require_admin
from .model import ProductCreate

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("")
def list_products(request: Request):
    return service.get_products(dict(request.query_params))

@router.post("")
def create_product(product: ProductCreate, admin=Depends(require_admin)):
    try:
        service.save(product.model_dump())
        return {"message": "Product created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
def delete_product(product_id: int, admin=Depends(require_admin)):
    try:
        return service.delete(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/filters")
def get_filters(category: str | None = Query(None)):
    try:
        return service.get_filter_options(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))