from typing import Optional
from fastapi import FastAPI, Header, APIRouter, Depends, HTTPException, status

async def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

router = APIRouter(dependencies=[Depends(secret_header)])

@router.get("/route1")
async def router_route1():
    return {"route": "router1"}

@router.get("/route2")
async def router_route2():
    return {"route": "router2"}


app = FastAPI()
app.include_router(router, prefix="/router")