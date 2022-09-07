from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

app = FastAPI()


@app.get('/html', response_class=HTMLResponse)
async def get_html():
    
    return """
    <html>
    <head><title>Hello World!</title></head>
    <body><h1>Hello World!</h1></body>
    </html>
    """

@app.get("/text", response_class=PlainTextResponse)
async def text():
    return "Hello World!"
