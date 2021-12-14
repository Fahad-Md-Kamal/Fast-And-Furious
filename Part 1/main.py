from fastapi import (FastAPI, 
Query, Body, 
Cookie, Header, 
Form, File, UploadFile, 
responses, Request)
from fastapi.param_functions import Depends
import requests
from enum import Enum
from typing import List, Optional, Set, Dict
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID
from datetime import datetime, time, timedelta

app = FastAPI()


fake_items_db = [
    {"item_name": "Foo"}, 
    {"item_name": "Bar"}, 
    {"item_name": "Baz"}
    ]





class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return responses.JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Image(BaseModel):
    url: HttpUrl #= Field(..., example="http://127.0.0.1:8000/")
    name: str #= Field(None, example="Facebook Profile Image")


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="The description of the item", max_length=2000)
    price: float
    tax: Optional[float] = None
    tags: Optional[List[str]] = None
    image: Optional[List[Image]] = None

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 35.4,
    #             "tax": 3.2,
    #             "tags": [
    #                 "tag 1",
    #                 "tag 2"
    #                 ],
    #             "image": [
    #                 {
    #                     "url": "http://127.0.0.1:8000",
    #                     "name": "example image"
    #                 }
    #             ]
    #         }
    #     }


class UserIn(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    full_name: Optional[str] = None

class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(files: List[UploadFile] = File(...)):
    return {"filename": [file.filename for file in files]}


@app.post("/login/", summary="User's Login", description="Enter the Username and password that you have provided to access the account")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


@app.put("/items/{item_id}")
async def read_items(
    item_id: int,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
    commons: dict = Depends(common_parameters)
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
    
@app.get("/")
async def root(user_agent: Optional[str] = Header(None)):
    r = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/grave")
    return {"message": "Bismillahir Rahmanir Rahim", "resp":r.text}

@app.get("/item/{id}")
async def item_detail(id:int = Cookie(None), ):
    return {"message": id}

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user

@app.post('/items/')
async def create_item(item:Item = Body(...,  examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        })):
    return item

# @app.put('/items/{item_id}')
# async def create_item(item_id: int, item:Item):
#     return {"item_id":item_id, **item.dict()}

@app.put("/items-q/{item_id}")
async def create_item(item_id: int, item: Item =Body(..., 
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        }),
        response_description = "The created Item",
        q: Optional[str] = None,
    commons: dict = Depends(common_parameters)
    ):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items-tags/", tags=["items"])
async def read_items():
    return {"items":fake_items_db}

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]

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


@app.get("/read-items-title/")
async def read_items_title(q: Optional[List[str]] = Query(["foo", "bar"], ), 
    title="Enter a Query String", 
    description="Query string for the items to search in the database that have a good match", 
    size: float = Query(..., gt=0, lt=10.5)
    ):
    results = {"q": q, 'title':title, 'description': description, 'size': size}
    return results


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

# @app.put("/item-user/{item_id}")
# async def update_item(item_id: int, item: Item, user: User, importance: int = Body(...)):
#     fake_items_db.append(item)
#     results = {"item_id": item_id, "item": item, "user": user, 'importance': importance, "fk_items":fake_items_db}
#     return results


@app.put("/item-user/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results