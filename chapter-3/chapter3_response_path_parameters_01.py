from fastapi import FastAPI, status
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def get_request_object(post: Post):
    return post
