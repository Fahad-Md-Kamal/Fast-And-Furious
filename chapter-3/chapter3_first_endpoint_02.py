from fastapi import FastAPI

app = FastAPI()

@app.get('/users/{type}/{id}/')
async def get_user_by_type(type: str, id: int):
    return {"type": type, "id": id}
