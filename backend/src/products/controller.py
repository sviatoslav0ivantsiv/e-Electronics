from fastapi import APIRouter, HTTPException, Depends, Query
from . import service
from src.auth.controller import require_admin
from .model import ProductCreate, ProductPatch, product_filter_params
from src.rate_limiting import limiter
from fastapi import Request


router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("")
@limiter.limit("5/minute")
def list_products(request: Request, filters: dict = Depends(product_filter_params)):
    return service.get_products(filters)

@router.get("/filters")
@limiter.limit("5/minute")
def get_filters(request: Request, category: str | None = Query(None)):
    try:
        return service.get_filter_options(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{product_id}")
@limiter.limit("5/minute")
def get_product(request: Request, product_id: int):
    try:
        product = service.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
@limiter.limit("5/minute")
def create_product(request: Request, product: ProductCreate, admin=Depends(require_admin)):
    try:
        service.save(product.model_dump())
        return {"message": "Product created"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{product_id}")
@limiter.limit("5/minute")
def update_product(request: Request, product_id: int, product: ProductCreate, admin=Depends(require_admin)):
    try:
        service.update(product_id, product.model_dump(exclude_none=True))
        return {"message": "Product updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/{product_id}")
@limiter.limit("5/minute")
def patch_product(request: Request, product_id: int, product: ProductPatch, admin=Depends(require_admin)):
    try:
        service.update(product_id, product.model_dump(exclude_unset=True))
        return {"message": "Product partially updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
@limiter.limit("5/minute")
def delete_product(request: Request, product_id: int, admin=Depends(require_admin)):
    try:
        return service.delete(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

