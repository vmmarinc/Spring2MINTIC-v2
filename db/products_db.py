from pydantic import BaseModel
from typing import  Dict

class ProductsInDB(BaseModel):
    bar_code        :   str
    name            :   str
    price           :   int
    stock           :   int

class ProductsInDB2(BaseModel):
    bar_code        :   str
    stock           :   int

#Base de Datos Ficticia 
database_products = Dict[str, ProductsInDB]
database_products = {

    "123_456": ProductsInDB(**{"bar_code":"123_456",
                                "name":"Torta 1",
                                "price":12000,
                                "stock":100}),

    "123_457": ProductsInDB(**{"bar_code":"123_457",
                                "name":"Torta 2",
                                "price":6000,
                                "stock":100}),

}

def save_product(product_in_db: ProductsInDB):
    database_products[product_in_db.bar_code] = product_in_db
    return product_in_db

def get_product(bar_code_product: str):
    if bar_code_product in database_products.keys():
        return database_products[bar_code_product]
    else:
        return None

def get_all_products():
    return database_products.values()
