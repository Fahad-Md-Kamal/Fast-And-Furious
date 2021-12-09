from fastapi import FastAPI, Query
import requests
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()


fake_items_db = [
    {"item_name": "Foo"}, 
    {"item_name": "Bar"}, 
    {"item_name": "Baz"}
    ]

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name:str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
async def root():
    r = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/grave")
    return {"message": "Bismillahir Rahmanir Rahim", "resp":r.text}

@app.get("/item/{id}")
async def item_detail(id:int):
    return {"message": id}

@app.post('/items/')
async def create_item(item:Item):
    return item

@app.put('/items/{item_id}')
async def create_item(item_id: int, item:Item):
    return {"item_id":item_id, **item.dict()}

@app.put("/items-q/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    # Request body + path + query parameters
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

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

# @app.get("/read-items/")
# async def read_items(q: Optional[str] = Query(..., max_length=50, min_length=3, regex="^fixedquery$")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/read-items/")
# async def read_items(q: Optional[List[str]] = Query(None)):
#     results = {"q": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     return results


# @app.get("/read-items/")
# async def read_items(q: Optional[List[str]] = Query(["foo", "bar"]), title="Query String", description="Query string for the items to search in the database that have a good match"):
#     results = {"q": q}
#     return results


@app.get("/read-items/")
async def read_items(q: Optional[List[str]] = Query(
    None, 
    alias="item-query", deprecated=True
    )):
    results = {"q": q}
    return results


# @app.get("/items/")
# async def read_items(q: Optional[List[str]] = Query(None)):
#     query_items = {"q": q}
#     return query_items


@app.get("/items/{item_id}/")
async def read_item_detail(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
    
@app.get("/items-read/{item_id}")
async def read_item_typeconvo(item_id: str, q: Optional[str] = None, short:bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/needy/{item_id}")
async def read_user_needt_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

# https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/