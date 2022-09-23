from typing import Any, Dict

import httpx
from fastapi import FastAPI, Depends

app = FastAPI()

class ExternalAPI:

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url="https://dummy.restapiexample.com/api/v1/"
        )
    
    async def __call__(self) -> dict[str]:
        async with self.client as client:
            response = await client.get("employees")
            return response.json()
        
external_api = ExternalAPI()

@app.get("/employees")
async def external_employees(employees: dict[str, any] = Depends(external_api)):
    return employees