from fastapi import APIRouter, HTTPException, Depends, Query
from . import service
from src.auth.controller import require_admin
from .model import ProductCreate, product_filter_params


router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("")
def list_products(filters: dict = Depends(product_filter_params)):
    return service.get_products(filters)

@router.get("/filters")
def get_filters(category: str | None = Query(None)):
    try:
        return service.get_filter_options(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
def create_product(product: ProductCreate, admin=Depends(require_admin)):
    try:
        service.save(product.model_dump())
        return {"message": "Product created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{product_id}")
def update_product(product_id: int, product: ProductCreate, admin=Depends(require_admin)):
    try:
        service.update(product_id, product.model_dump(exclude_none=True))
        return {"message": "Product updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/{product_id}")
def patch_product(product_id: int, product: ProductCreate, admin=Depends(require_admin)):
    try:
        service.update(product_id, product.model_dump(exclude_unset=True))
        return {"message": "Product partially updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
def delete_product(product_id: int, admin=Depends(require_admin)):
    try:
        return service.delete(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

