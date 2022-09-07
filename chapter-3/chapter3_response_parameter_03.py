from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app2 = FastAPI()

class Post(BaseModel):
    title: str
    nb_views: int

posts = {
    1: Post(title="Hello", nb_views=100)
}

@app2.post('/posts/{id}')
async def update_or_create_post(id: int, post: Post, response: Response):
    if id not in posts:
        posts[id] = post
        response.status_code = status.HTTP_201_CREATED
    return posts[id]
