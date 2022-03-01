from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db
from .utils import hash_pwd

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post, tags=['POST'])
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """ Create Posts """
    
    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.get("/posts", response_model= List[schemas.Post], tags=['POST'])
async def get_posts(db: Session = Depends(get_db)):
    """ Return All Posts """
    
    posts = db.query(models.Post).all()
    
    return posts


@app.get("/posts/{id}", response_model= schemas.Post, tags=['POST'])
async def get_post(id: int, db: Session = Depends(get_db)):
    """ Return Single Post """
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")
    
    return post.first()


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['POST'])
async def delete_post(id: int, db: Session = Depends(get_db)):
    """ Delete Post """
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model= schemas.Post, status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
async def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """ Update a Post """
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=['USER'])
async def create_post(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Register User """
    user = db.query(models.User).filter(
        (models.User.email == user_data.email) |
        (models.User.username == user_data.username)
    )

    if user.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with this Email/ Username already exists.")

    hashed_password = hash_pwd(user_data.password)
    user_data.password = hashed_password

    user = models.User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@app.get('/user/{id}', response_model= schemas.UserResponse, tags=['USER'])
async def get_user(id:int, db: Session=Depends(get_db)):
    """ Get User Detail """
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: '{id}' Not-Found")
    return user.first()
