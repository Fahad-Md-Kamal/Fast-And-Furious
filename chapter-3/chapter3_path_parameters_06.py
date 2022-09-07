from fastapi import FastAPI, Path

app = FastAPI()

@app.get('/license-plates/{license}')
async def get_user(license : str = Path(..., regex=f"^\w{2}-\d{3}-\w{2}$")):
    return {"license": license}

