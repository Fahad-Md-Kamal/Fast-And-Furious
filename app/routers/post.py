from typing import List, Optional
from fastapi import (
    Depends,
    Response,
    status,
    HTTPException,
    APIRouter
)
from sqlalchemy.orm import Session

from app import oauth2

from .. import models, schemas
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=["POST"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    """ Create Posts """

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@router.get("/", response_model=List[schemas.Post])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(oauth2.get_current_user),
    limit: int = 10, 
    skip: int = 0, 
    search: Optional[str] = ""
    ):
    """ Return All Posts """
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    """ Return Single Post """

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")

    return post.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    """ Delete Post """

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the action")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post, status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
async def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    """ Update a Post """

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the action")    

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
