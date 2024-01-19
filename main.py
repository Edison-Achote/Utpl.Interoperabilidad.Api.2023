from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
#importar librerias para el manejo de la base de datos pymongo
import pymongo

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://Eachote:241993@cluster0.ovxftp8.mongodb.net/?retryWrites=true&w=majority")
database = cliente["Vendedor"]
coleccion = database["Vendedor"]
app = FastAPI(
    title="API de vendedores",
    description="API para vendedore",
    version="1.0.1",
    contact={
        "name": "Edison Achote ",
        "email": "erachote@gmail.com",
        "url": "https://github.com/Edison-Achote/Utpl.Interoperabilidad.Api.2023"
    },
    license_info={
        "name": "MIT License",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    openapi_tags=[
        {
            "name": "Vendedores",
            "description": "Operaciones para el manejo de personas"
        }
    ]
)

# Modelo de datos para un vendedor
class Seller(BaseModel):
    name: str
    age: int
    email: str
    id: int
    identification: str
    city: str

# Lista para almacenar vendedores (simulación de base de datos)
sellers_db = []

# Operación para crear un vendedor
@app.post("/vendedor/", response_model=Seller,tags=["Vendedores"])
def create_seller(seller: Seller):
    result = coleccion.insert_one(seller.dict())
    return seller

# Operación para obtener todos los vendedores
@app.get("/vendedor/", response_model=List[Seller],tags=["Vendedores"])
def get_all_sellers():
    return sellers_db

# Operación para obtener un vendedor por ID
@app.get("/vendedor/{seller_id}", response_model=Seller,tags=["Vendedores"])
def get_seller_by_id(seller_id: int):
    for seller in sellers_db:
        if seller.id == seller_id:
            return seller
    raise HTTPException(status_code=404, detail="Vendedor no encontrado")

# Operación para editar un vendedor por ID
@app.put("/vendedor/{seller_id}", response_model=Seller,tags=["Vendedores"])
def update_seller(seller_id: int, updated_seller: Seller):
    for index, seller in enumerate(sellers_db):
        if seller.id == seller_id:
            sellers_db[index] = updated_seller
            return updated_seller
    raise HTTPException(status_code=404, detail="Vendedor no encontrado")

# Operación para eliminar un vendedor por ID
@app.delete("/vendedor/{seller_id}", response_model=Seller,tags=["Vendedores"])
def delete_seller(seller_id: int):
    for index, seller in enumerate(sellers_db):
        if seller.id == seller_id:
            deleted_seller = sellers_db.pop(index)
            return deleted_seller
    raise HTTPException(status_code=404, detail="Vendedor no encontrado")
