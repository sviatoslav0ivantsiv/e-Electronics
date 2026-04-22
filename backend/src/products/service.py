from src.database.core import get_connection

def get_products(filters: dict):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql = ""
    params = []
    

    LIKE = "LIKE"

    single_filters = [
        ("category", "category", "="),
        ("min_price", "price", ">="),
        ("max_price", "price", "<="),
        ("model", "model", LIKE),
        ("min_display_size", "display_size", ">="),
        ("max_display_size", "display_size", "<="),
        ("min_battery_capacity", "battery_capacity", ">="),
        ("max_battery_capacity", "battery_capacity", "<="),
        ("min_screen_size", "screen_size", ">="),
        ("max_screen_size", "screen_size", "<="),
        ("min_weight", "weight", ">="),
        ("max_weight", "weight", "<="),
        ("min_battery_life", "battery_life", ">="),
        ("max_battery_life", "battery_life", "<="),
    ]

    for filter_key, field, operator in single_filters:
        val = filters.get(filter_key)
        if val is not None:
            sql += f" AND {field} {operator} %s"
            params.append(f"%{val}%" if operator is LIKE else val)
    
    list_filters = ["brand", "camera_mp", "cpu", "gpu", "screen_type", "water_resistance", "ram", "storage"]

    for field in list_filters:
        val = filters.get(field)
        if val is not None:
            items = val if isinstance(val, list) else [val]
            placeholders = ', '.join(['%s'] * len(items))
            sql += f" AND {field} IN ({placeholders})"
            params.extend(items)
    
    limit = min(int(filters.get("limit", 10)), 100)
    offset = (int(filters.get("page", 1)) - 1) * limit
    direction = filters.get("sort", "DESC").upper()

    select_sql ="SELECT * FROM products WHERE 1=1" + sql + f" ORDER BY price {direction}" + " LIMIT %s OFFSET %s"
    cursor.execute(select_sql, params + [limit, offset])
    products = cursor.fetchall()

    count_sql = "SELECT COUNT(*) as total FROM products WHERE 1=1" + sql
    cursor.execute(count_sql, params)
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()
    return {"products": products, "total": total}

def save(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    
    clean_data = {k: v for k, v in data.items() if v is not None}
    columns = ", ".join(clean_data.keys())
    placeholders = ", ".join(["%s"] * len(clean_data))
    
    sql = f"INSERT INTO products ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(clean_data.values()))
    
    conn.commit()
    cursor.close()
    conn.close()

def update(product_id, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    clean_data = {k: v for k, v in data.items() if v is not None}
    columns = ", ".join([f"{k}=%s" for k in clean_data.keys()])

    sql = f"UPDATE products SET {columns} WHERE id=%s"
    cursor.execute(sql, list(clean_data.values()) + [product_id])

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Product updated"}

def delete(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return {"message": "Product deleted"}

def get_filter_options(category=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    where = "WHERE category = %s" if category else ""
    params = [category] if category else []
    fields = ["brand", "ram", "storage"]

    if category == "laptop":
        fields += ["cpu", "gpu"]
    elif category == "smartphone":
        fields += ["camera_mp"]
    elif category == "smartwatch":
        fields += ["screen_type", "water_resistance"]

    result = {}

    for col in fields:
        cursor.execute(f"SELECT DISTINCT {col} FROM products {where} ORDER BY {col}", params)
        result[col] = [row[col] for row in cursor.fetchall() if row[col] is not None]

    cursor.close()
    conn.close()
    return result