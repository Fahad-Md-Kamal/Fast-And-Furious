from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    nb_views: int

posts = {
    1: Post(title="Hello", nb_views=100)
}


@app.get('/posts/{id}')
async def get_post(id: int):
    return posts[id]
