from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI()

class Product(BaseModel):
    name: str
    price: int
    date_added: date

products = [Product(name="Macbook", price=2000, date_added=date(2025, 1, 10))]

@app.get("/api")
def api_root():
    return {"name": "FastAPI"}

@app.get("/products")
def get_products() -> list[Product]:
    return products

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return product