from fastapi import FastAPI, Depends

app = FastAPI()

async def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return (skip, limit)

@app.get("/")
async def list_items(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}