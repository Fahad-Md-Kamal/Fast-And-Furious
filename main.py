from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    """ Responsible for maping Post Object's Data field """
    title: str
    content: str
    published: bool = True  # Assigning Default Value
    rating: Optional[int] = None  # Completely Optional Field


my_posts = [
    {"title": "Post One", "content": "Post One Content", "id": 1},
    {"title": "Post Two", "content": "Post Two Content", "id": 2}
]


@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['POST'])
# @app.post("/posts", tags=['POST'])
async def create_post(post: Post):
    """Create Posts"""
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 9999999)
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.get("/posts", tags=['POST'])
async def get_posts():
    """Return All Posts"""
    return {"data": my_posts}


@app.get("/posts/latest", tags=['POST'])
async def get_latest_post():
    """Return Sinngle Posts"""
    post = my_posts[len(my_posts)-1]
    return {"data": post}


@app.get("/posts/{id}", tags=['POST'])
# async def get_post(id:int, response: Response):
async def get_post(id: int):
    """Return Single Post"""
    for p in my_posts:
        if p['id'] == id:
            return {"data": p}
        else:
            # response.status_code = status.HTTP_404_NOT_FOUND
            # return {"message" : f"Post with ID: {id} Not Found"}
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} Not Found")
