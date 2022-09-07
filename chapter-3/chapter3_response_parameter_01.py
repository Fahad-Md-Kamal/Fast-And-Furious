from fastapi import FastAPI, Response

app = FastAPI()

@app.get('/')
async def get_post(response: Response):
    response.headers["Custom-Header"] = "Custom-Header-Value"
    return {"hello": "world"}
