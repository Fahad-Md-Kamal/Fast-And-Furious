from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    """ Responsible for maping Post Object's Data field """
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi_db',
            user='genex',
            password='postgres',
            cursor_factory=RealDictCursor
        )
        print("database Connection was successfull")
        cursor = conn.cursor()
        break
    except Exception as error:
        print("database Connection was Faild")
        print("Error", error)
        time.sleep(2)


@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['POST'])
async def create_post(post: Post):
    """Create Posts"""

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.get("/posts", tags=['POST'])
async def get_posts():
    """Return All Posts"""

    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {"data": posts}


@app.get("/posts/{id}", tags=['POST'])
async def get_post(id: int):
    """Return Single Post"""

    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),))
    post = cursor.fetchone()

    if post:
        return {"data": post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post Not-Found"
        )


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['POST'])
async def delete_post(id: int):
    """ Delete Post With The Given Id"""

    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post Not-Found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
async def update_post(id: int, post: Post):
    """Update a Post with the payload"""

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post Not-Found"
        )

    return {"data": post}
