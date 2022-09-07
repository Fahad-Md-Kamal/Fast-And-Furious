from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    nb_views: int

class PublicPost(BaseModel):
    title: str

posts = {
    1: Post(title="Hello", nb_views=100)
}


@app.get('/posts/{id}', response_model=PublicPost)
async def get_post(id: int):
    return posts[id]
