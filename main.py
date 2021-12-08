from fastapi import FastAPI
import requests
from enum import Enum
from typing import Optional

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
async def root():
    r = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/grave")
    return {"message": "Bismillahir Rahmanir Rahim", "resp":r.text}

@app.get("/item/{id}")
async def item_detail(id:int):
    return {"message": id}

@app.get("/users/me}")
async def read_user_me():
    return {"user_id": "The Current User"}

@app.get("/users/{user_id}")
async def read_user(user_id:str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
    
@app.get("/items/{item_id}")
async def read_item_detail(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}