from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/redirect")
async def redirect():
    return RedirectResponse("/new-url")

@app.get("/new-url")
async def new_url():
    return "Redurected"