from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos para un vendedor
class Seller(BaseModel):
    name: str
    age: int
    email: str
    id: int

# Lista para almacenar vendedores (simulación de base de datos)
sellers_db = []

# Operación para crear un vendedor
@app.post("/vendedor/", response_model=Seller)
def create_seller(seller: Seller):
    sellers_db.append(seller)
    return seller

# Operación para obtener todos los vendedores
@app.get("/vendedor/", response_model=List[Seller])
def get_all_sellers():
    return sellers_db

# Operación para obtener un vendedor por ID
@app.get("/vendedor/{seller_id}", response_model=Seller)
def get_seller_by_id(seller_id: int):
    for seller in sellers_db:
        if seller.id == seller_id:
            return seller
    raise HTTPException(status_code=404, detail="Vendedor no encontrado")

# Operación para editar un vendedor por ID
@app.put("/vendedor/{seller_id}", response_model=Seller)
def update_seller(seller_id: int, updated_seller: Seller):
    for index, seller in enumerate(sellers_db):
        if seller.id == seller_id:
            sellers_db[index] = updated_seller
            return updated_seller
    raise HTTPException(status_code=404, detail="Vendedor no encontrado")

# Operación para eliminar un vendedor por ID
@app.delete("/vendedor/{seller_id}", response_model=Seller)
def delete_seller(seller_id: int):
    for index, seller in enumerate(sellers_db):
        if seller.id == seller_id:
            deleted_seller = sellers_db.pop(index)
            return deleted_seller
    raise HTTPException(status_code=404, detail="Vendedor no encontrado")
