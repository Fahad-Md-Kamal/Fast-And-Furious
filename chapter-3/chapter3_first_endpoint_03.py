from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class UserType(str, Enum):
    STANDARD = 'standard'
    ADMIN = 'admin'

@app.get('/users/{type}/{id}/')
async def get_user_by_type(type: UserType, id: int):
    return {"type": type, "id": id}
