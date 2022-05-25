from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserBase(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(BaseModel):
    """ Responsible for Allowing user's what data they can see """
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime]

class PostBase(BaseModel):
    """ Responsible for maping Post Object's Data field """
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    """ Responsible for Allowing user's what data they can see """
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)