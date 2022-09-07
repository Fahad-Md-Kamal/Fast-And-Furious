from fastapi import FastAPI, Response

app2 = FastAPI()

@app2.get('/')
async def custom_cookie(response: Response):
    response.set_cookie("cookie-name", "cookie-value", max_age=86400)
    return {"hello": "world"}
