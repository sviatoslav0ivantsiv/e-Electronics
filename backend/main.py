from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from models import Product

app = FastAPI()

# ✅ ДОДАЙ СЮДИ СВІЙ IP
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.7:3000",  # 🔥 ВАЖЛИВО
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # дозволяє OPTIONS (preflight)
    allow_headers=["*"],
)

# ------------------- ROUTES -------------------

@app.get("/api/products")
def get_products(category: str | None = Query(None), page: int = Query(1), limit: int = Query(10)):
    try:
        if category:
            return Product.by_category(category, page, limit)
        return Product.paginate(page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/products")
def create_product(data: dict = Body(...)):
    try:
        product = Product(**data)
        product.save()
        return {"message": "Product created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/admin/products/{product_id}")
def update_product(product_id: int, data: dict = Body(...)):
    try:
        return Product.update(product_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/api/admin/products/{product_id}")
def patch_product(product_id: int, data: dict = Body(...)):
    try:
        return Product.patch(product_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/admin/products/{product_id}")
def delete_product(product_id: int):
    try:
        return Product.delete(product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))