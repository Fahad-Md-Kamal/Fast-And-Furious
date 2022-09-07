from enum import Enum
from fastapi import FastAPI

app = FastAPI()


class UserType(str, Enum):
    STANDARD = 'standard'
    ADMIN = 'admin'

@app.get('/')
async def hello_world():
    return {"hello":"World"}

@app.get('/users/{type}/{id}/')
async def get_user_by_type(type: UserType, id: int):
    return {"type": type, "id": id}


@app.get('/users/{id}')
async def get_user(id : int):
    return {"id": id}

