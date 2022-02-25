from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()


class Post(BaseModel):
    """ Responsible for maping Post Object's Data field """
    title: str
    content: str
    published: bool = True  # Assigning Default Value

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_db', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        print("database Connection was successfull")
        cursor = conn.cursor()
        break
    except Exception as error:
        print("database Connection was Faild")
        print("Error", error)
        time.sleep(2)

my_posts = [
    {"title": "Post One", "content": "Post One Content", "id": 1},
    {"title": "Post Two", "content": "Post Two Content", "id": 2}
]


def find_post(id):
    """Return post contains the id"""
    for p in my_posts:
        if p['id'] == id:
            return p


def find_post_index(id: int):
    """Return Index of the Matching post item."""
    for idx, val in enumerate(my_posts):
        if val['id'] == id:
            return idx


@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['POST'])
async def create_post(post: Post):
    """Create Posts"""
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 9999999)
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.get("/posts", tags=['POST'])
async def get_posts():
    """Return All Posts"""
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/latest", tags=['POST'])
async def get_latest_post():
    """Return Sinngle Posts"""
    post = my_posts[len(my_posts)-1]
    return {"data": post}


@app.get("/posts/{id}", tags=['POST'])
async def get_post(id: int):
    """Return Single Post"""
    post = find_post(id)
    if post:
        return {"data": post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not-Found")


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['POST'])
async def delete_post(id: int):
    """ Delete Post With The Given Id"""
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not-Found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
async def update_post(id: int, post: Post):
    """Update a Post with the payload"""
    index = find_post_index(id)  # Check if Post exists with the given id
    if index == None:  # If not exists rais error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not-Found")
    post_dict = post.dict()  # Convert the payload post to dictonary
    post_dict['id'] = id  # Assign the post it to the converted dictionary
    my_posts[index] = post_dict  # replace the post item in the list
    return {"message": post_dict}
