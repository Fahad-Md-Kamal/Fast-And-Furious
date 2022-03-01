from fastapi import (
    Depends,
    status,
    HTTPException,
    APIRouter
)
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=['USER']
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_post(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Register User """
    user = db.query(models.User).filter(
        (models.User.email == user_data.email) |
        (models.User.username == user_data.username)
    )

    if user.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with this Email/ Username already exists.")

    hashed_password = utils.hash_pwd(user_data.password)
    user_data.password = hashed_password

    user = models.User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    """ Get User Detail """
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: '{id}' Not-Found")
    return user.first()
