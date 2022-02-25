# FastAPI Blog Application

### Setup 
- Install FastAPI
```sh
pip install fastapi
```
- Install development server
```sh
pip install "uvicorn[standard]"
```

### Part - One [Git Commit](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/commit/885189adc7e261a41a52b3f600ca8c9c71d7c203)
- Basics of FastAPI
- Basic GET and POST request

```python
from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()

@app.get("/", tags=['POST'])
async def home_view():
    return {"message": "In the name of Allah, I'm beginning"}

@app.post("/create-post", tags=['POST'])
async def create_post(payload: dict=Body(...)):

    return {"new_post" : "Post Created Successfully"}
```

### Part - Two [Git Commit](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/commit/ce621b2924ed8854e747c504dacbaf272642f795)
- Basic Data Model using Pydentic lib
- Making Optional model field
- Assining Default value to the model fild.

```python
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    """ Responsible for maping payload Data """
    title: str
    content: str
    published: bool = True # Assigning Default Value
    rating: Optional[int] = None # Completely Optional Field

@app.post("/create-post", tags=['POST'])
async def create_post(post:Post):
    print(post.dict())
    return {"data":"Post Created Successfully"}  
```