from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint, constr, confloat, EmailStr
from typing import Optional

app = FastAPI()

users = []
items = []

class User(BaseModel):
    id: int
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    age: Optional[conint(ge=18, le=100)] = None


class UserCreate(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    age: Optional[conint(ge=18, le=100)] = None



class Item(BaseModel):
    id: int
    title: constr(min_length=2, max_length=100)
    description: Optional[constr(max_length=500)] = None
    price: confloat(gt=0)


class ItemCreate(BaseModel):
    title: constr(min_length=2, max_length=100)
    description: Optional[constr(max_length=500)] = None
    price: confloat(gt=0)





@app.get("/")
async def hello():
    return {"massage": "Welcome to the FastAPI project👋"}


@app.post("/users")
def user_create(user: UserCreate):
    user_id = len(users)+1
    new_user = User(id=user_id, **user.dict())
    users.append(new_user)
    return new_user


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Task not found ")



@app.post("/items")
def item_create(item: ItemCreate):
    item_id = len(items)+1
    new_item = Item(id=item_id, **item.dict())
    items.append(new_item)
    return new_item

@app.get("/items/{item_id}")
def get_items(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Task not found ")
