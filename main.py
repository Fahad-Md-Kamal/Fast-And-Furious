from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    """ Responsible for maping Post Object's Data field """
    title: str
    content: str
    published: bool = True # Assigning Default Value
    rating: Optional[int] = None # Completely Optional Field

@app.get("/", tags=['POST'])
async def home_view():
    return {"message": "Bismiallahir Rahmanir Rahim"}


@app.post("/create-post", tags=['POST'])
async def create_post(post:Post):
    print(post.dict())
    return {"data":"Post Created Successfully"}
