from src.database.core import get_connection

def get_products(filters: dict):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql = ""
    params = []
    
    if filters.get("category"):
        sql += " AND category = %s"
        params.append(filters["category"])
    if filters.get("brand"):
        if isinstance(filters["brand"], list):
            placeholders = ', '.join(['%s'] * len(filters["brand"]))
            sql += f" AND brand IN ({placeholders})"
            params.extend(filters["brand"])
        else:
            sql += " AND brand = %s"
            params.append(filters["brand"])
    if filters.get("min_price"):
        sql += " AND price >= %s"
        params.append(filters["min_price"])
    if filters.get("max_price"):
        sql += " AND price <= %s"
        params.append(filters["max_price"])
    if filters.get("model"):
        sql += " AND model LIKE %s"
        params.append(f"%{filters['model']}%")
    if filters.get("min_display_size"):
        sql += " AND display_size >= %s"
        params.append(filters["min_display_size"])
    if filters.get("max_display_size"):
        sql += " AND display_size <= %s"
        params.append(filters["max_display_size"])
    if filters.get("min_battery_capacity"):
        sql += " AND battery_capacity >= %s"
        params.append(filters["min_battery_capacity"])
    if filters.get("max_battery_capacity"):
        sql += " AND battery_capacity <= %s"
        params.append(filters["max_battery_capacity"])
    if filters.get("camera"):
        if isinstance(filters["camera"], list):
            placeholders = ', '.join(['%s'] * len(filters["camera"]))
            sql += f" AND camera_mp IN ({placeholders})"
            params.extend(filters["camera"])
        else:
            sql += " AND camera_mp = %s"
            params.append(filters["camera"])
    if filters.get("cpu"):
        if isinstance(filters["cpu"], list):
            placeholders = ', '.join(['%s'] * len(filters["cpu"]))
            sql += f" AND cpu IN ({placeholders})"
            params.extend(filters["cpu"])
        else:
            sql += " AND cpu = %s"
            params.append(filters["cpu"])
    if filters.get("gpu"):
        if isinstance(filters["gpu"], list):
            placeholders = ', '.join(['%s'] * len(filters["gpu"]))
            sql += f" AND gpu IN ({placeholders})"
            params.extend(filters["gpu"])
        else:
            sql += " AND gpu = %s"
            params.append(filters["gpu"])
    if filters.get("min_screen_size"):
        sql += " AND screen_size >= %s"
        params.append(filters["min_screen_size"])
    if filters.get("max_screen_size"):
        sql += " AND screen_size <= %s"
        params.append(filters["max_screen_size"])
    if filters.get("min_weight"):
        sql += " AND weight >= %s"
        params.append(filters["min_weight"])
    if filters.get("max_weight"):
        sql += " AND weight <= %s"
        params.append(filters["max_weight"])
    if filters.get("screen_type"):
        if isinstance(filters["screen_type"], list):
            placeholders = ', '.join(['%s'] * len(filters["screen_type"]))
            sql += f" AND screen_type IN ({placeholders})"
            params.extend(filters["screen_type"])
        else:
            sql += " AND screen_type = %s"
            params.append(filters["screen_type"])
    if filters.get("min_battery_life"):
        sql += " AND battery_life >= %s"
        params.append(filters["min_battery_life"])
    if filters.get("max_battery_life"):
        sql += " AND battery_life <= %s"
        params.append(filters["max_battery_life"])
    if filters.get("water_resistance"):
        if isinstance(filters["water_resistance"], list):
            placeholders = ', '.join(['%s'] * len(filters["water_resistance"]))
            sql += f" AND water_resistance IN ({placeholders})"
            params.extend(filters["water_resistance"])
        else:
            sql += " AND water_resistance = %s"
            params.append(filters["water_resistance"])
    if filters.get("ram"):
        if isinstance(filters["ram"], list):
            placeholders = ', '.join(['%s'] * len(filters["ram"]))
            sql += f" AND ram IN ({placeholders})"
            params.extend(filters["ram"])
        else:
            sql += " AND ram = %s"
            params.append(filters["ram"])
    if filters.get("storage"):
        if isinstance(filters["storage"], list):
            placeholders = ', '.join(['%s'] * len(filters["storage"]))
            sql += f" AND storage IN ({placeholders})"
            params.extend(filters["storage"])
        else:
            sql += " AND storage = %s"
            params.append(filters["storage"])
    
    limit = int(filters.get("limit", 10))
    limit = min(limit, 100)
    page = int(filters.get("page", 1))
    offset = (page - 1) * limit
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