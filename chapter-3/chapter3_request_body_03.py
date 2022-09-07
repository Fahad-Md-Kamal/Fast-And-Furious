from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int


class Company(BaseModel):
    name: str


@app.post('/users')
async def create_user(user: User, company: Company):
    return {"user": user, "company": company}
