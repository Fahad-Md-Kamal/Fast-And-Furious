from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostPartialUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None

class PostPublic(PostBase):
    id: int

class PostDB(PostBase):
    id: int
    nb_views: int = 0


class DummyDatabase:
    posts: dict[int, PostDB] = {}

db = DummyDatabase()
app = FastAPI()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostPublic)
async def create(post_create: PostCreate):
    new_id = max(db.posts.keys() or (0,)) + 1

    post = PostDB(id=new_id, **post_create.dict())

    db.posts[new_id] = post
    return post


@app.patch("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=PostPublic)
async def partial_update(id: int, post_update: PostPartialUpdate):
    try:
        post_db = db.posts[id]

        updated_fields = post_update.dict(exclude_unset=True)
        updated_post = post_db.copy(update=updated_fields)
        db.posts[id] = updated_post
        return updated_post
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)