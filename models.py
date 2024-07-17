from fastapi import FastAPI
from pydantic import BaseModel, conint, constr, confloat, field_validator
from typing import Optional, Any


app = FastAPI()


class User(BaseModel):
    id: int
    name: constr(min_length=2, max_length=50)
    age: Optional[conint(ge=18, le=100)] = None


class Item(BaseModel):
    id: int
    title: constr(min_length=2, max_length=100)
    description: Optional[constr(max_length=500)] = None
    price: confloat(gt=0)


    @field_validator('age')
    @classmethod
    def price_must_be_positive(cls, value: Any):
        if value is not None and not (18 <= value <= 100):
            raise ValueError('вік має бути від 18 до 100 років')
        return value


    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, value: Any):
        if value <= 0:
            raise ValueError("Ціна повинна бути більшою за нуль")
        return value