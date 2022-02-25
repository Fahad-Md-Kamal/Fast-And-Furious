from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()

@app.get("/", tags=['POST'])
async def home_view():
    return {"message": "Bismiallahir Rahmanir Rahim"}

@app.post("/create-post", tags=['POST'])
async def create_post(payload: dict=Body(...)):

    return {"new_post" : f"title: {payload['title']} content: {payload['content']}"}
    