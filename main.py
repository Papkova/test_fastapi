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


class UserUpdate(BaseModel):
    name: Optional[constr(min_length=2, max_length=50)] = None
    email: Optional[EmailStr] = None
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


class ItemUpdate(BaseModel):
    title: Optional[constr(min_length=2, max_length=100)] = None
    description: Optional[constr(max_length=500)] = None
    price: Optional[confloat(gt=0)] = None



@app.get("/")
async def hello():
    return {"massage": "Welcome to the FastAPI project👋"}


@app.post("/users")
def user_create(user: UserCreate):
    user_id = len(users)+1
    new_user = User(id=user_id, **user.dict())
    users.append(new_user)
    return new_user


@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate):
    for user in users:
        if user.id == user_id:
            if user_update.name is not None:
                user.name = user_update.name
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.age is not None:
                user.age = user_update.age
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/items")
def item_create(item: ItemCreate):
    item_id = len(items)+1
    new_item = Item(id=item_id, **item.dict())
    items.append(new_item)
    return new_item


@app.put("/items/{items_id}")
def update_item(item_id: int, item_update: ItemUpdate):
    for item in items:
        if item.id == item_id:
            if item_update.title is not None:
                item.title = item_update.title
            if item_update.description is not None:
                item.description = item_update.description
            if item_update.price is not None:
                item.price = item_update.price
            return item
    raise HTTPException(status_code=404, detail="Item not found")