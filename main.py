from db.products_db import ProductsInDB
from db.products_db import get_product, get_all_products, save_product, database_products

from models.products_models import ProductIn, ProductOut, ProductIn2

from fastapi import FastAPI, HTTPException

api = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080","https://spring3-g2m3-6-app.herokuapp.com", 
]

api.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.post("/product/")
async def create_product(product_in: ProductIn):
    #Todas las comprobaciones Necesarias
    product_in_db = get_product(product_in.bar_code)

    if product_in_db != None:
        raise HTTPException(status_code=400, detail="La Categoria ya existe")
    
    #Guardando Categoria
    product_saved = save_product(ProductsInDB(**product_in.dict()))

    return ProductOut(**product_saved.dict())


@api.get("/product/{bar_code}")
async def get_product_bar_code(bar_code: str):
    #Buscar la categoria en la base datos
    product_in_db = get_product(bar_code)

    #Comprobar la respuesta
    if product_in_db == None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    #Retorna la categoria
    return ProductOut(**product_in_db.dict())


@api.put("/product/{bar_code}")
async def update_product(product_in: ProductIn):
    #Buscar la categoria en la base datos
    product_in_db = get_product(product_in.bar_code)

    #Comprobar la respuesta
    if product_in_db == None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    #Actualizar product
    product_updated = save_product(ProductsInDB(**product_in.dict()))

    #Retornando Respuesta
    return ProductOut(**product_updated.dict())


@api.put("/product/")
async def update_stock_product(product_in: ProductIn2):
    #Buscar la categoria en la base datos
    product_in_db = database_products[product_in.bar_code]
    

    #Comprobar la respuesta
    if product_in_db == None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    stockActual = product_in_db.stock
    stockVenta = product_in.stock

    stockNuevo = stockActual - stockVenta

    if stockNuevo < 0 | product_in_db == None:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    product_in_db.stock = stockNuevo

    #Actualizar product
    updated_product = save_product(product_in_db)
    
    #Retornando Respuesta
    return ProductOut(**updated_product.dict())

@api.get("/products/")
async def get_all():
    products_db = get_all_products()

    products_out = []
    for product_db in products_db:
        products_out.append(ProductOut(**product_db.dict()))

    return products_out
