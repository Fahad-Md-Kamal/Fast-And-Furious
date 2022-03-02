from datetime import datetime
from pydantic import BaseModel, EmailStr

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
    created_at: datetime

    class Config:
        orm_mode = True


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