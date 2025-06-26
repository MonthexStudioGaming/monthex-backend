from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"

def read_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file, "r") as f:
        return json.load(f)

def write_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# PRODUCTS
@app.get("/products")
def get_products():
    return read_json(PRODUCTS_FILE)

@app.post("/products")
def add_product(product: dict):
    products = read_json(PRODUCTS_FILE)
    product["id"] = len(products) + 1
    products.append(product)
    write_json(PRODUCTS_FILE, products)
    return {"message": "Product added"}

@app.put("/products/{product_id}")
def update_product(product_id: int, updated: dict):
    products = read_json(PRODUCTS_FILE)
    for p in products:
        if p["id"] == product_id:
            p.update(updated)
            write_json(PRODUCTS_FILE, products)
            return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    products = read_json(PRODUCTS_FILE)
    products = [p for p in products if p["id"] != product_id]
    write_json(PRODUCTS_FILE, products)
    return {"message": "Product deleted"}

# ORDERS
@app.post("/orders")
def place_order(order: dict):
    orders = read_json(ORDERS_FILE)
    order["id"] = len(orders) + 1
    orders.append(order)
    write_json(ORDERS_FILE, orders)
    return {"message": "Order placed"}

@app.get("/orders")
def get_all_orders():
    return read_json(ORDERS_FILE)

@app.get("/orders/user/{userid}")
def get_user_orders(userid: str):
    orders = read_json(ORDERS_FILE)
    return [o for o in orders if o["userid"] == userid]

@app.put("/orders/{order_id}")
def update_order(order_id: int, updated: dict):
    orders = read_json(ORDERS_FILE)
    for o in orders:
        if o["id"] == order_id:
            o.update(updated)
            write_json(ORDERS_FILE, orders)
            return {"message": "Order updated"}
    raise HTTPException(status_code=404, detail="Order not found")
