from pydantic import BaseModel

class ProductIn(BaseModel):
    bar_code        :   str
    name            :   str
    price           :   int
    stock           :   int

class ProductIn2(BaseModel):
    bar_code        :   str
    stock           :   int


class ProductOut(BaseModel):
    name            :   str
    price           :   int
    stock           :   int