import time
from fastapi import FastAPI

app = FastAPI()

@app.get("/fast")
async def fast():
    return {"endpoint": "fast"}

@app.get("/slow-async")
async def slow_async():
    time.sleep(10)
    return {"endpoint": "slow-async"}

@app.get("/slow-sync")
def slow_sync():
    time.sleep(10)
    return {"endpoint": "slow-sync"}