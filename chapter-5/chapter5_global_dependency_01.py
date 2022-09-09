from typing import Optional
from fastapi import FastAPI, Header, APIRouter, Depends, HTTPException, status

async def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

app = FastAPI(dependencies=[Depends(secret_header)])

@app.get("/route1")
async def router_route1():
    return {"route": "router1"}

@app.get("/route2")
async def router_route2():
    return {"route": "router2"}

