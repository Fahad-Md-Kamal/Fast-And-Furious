from dataclasses import fields
from pydantic import BaseModel, EmailStr
from tortoise.models import Model
from tortoise import fields

class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
    
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

class UserDB(User):
    hashed_password: str

class UserTortoise(Model):
    id = fields.IntField(pk=True, generated=True)
    email = fields.CharField(index=True, unique=True, null=False, max_length=255)
    hashed_password = fields.CharField(null=False, max_length=255)

    class Meta:
        table = "users"


