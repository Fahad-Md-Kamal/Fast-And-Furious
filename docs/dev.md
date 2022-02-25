### FastAPI Blog App Dev Documentation


### Part - One [Brows Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/885189adc7e261a41a52b3f600ca8c9c71d7c203)
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

### Part - Two [Brows Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/ce621b2924ed8854e747c504dacbaf272642f795)
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

## Part - Three [Brows File](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/)

- Return valid status code after object creation
    - Import status package from fastapi module
    - add "```status_code=status.HTTP_201_CREATED```" to the url decorator.
```python
from fastapi import FastAPI, status

@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['POST'])
async def create_post(post: Post):
    """Create Posts"""
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 9999999)
    my_posts.append(post_dict)
    return {"data": my_posts}
```
- Place the urls in perfect order hierarchy so that dynamic values do not replace an actual value of the request.

This comes first.
```python
@app.get("/posts/latest", tags=['POST'])
```
This comes later so that dynamic ```id``` is not replaced by ```latest``` value from the URL.
```python
@app.get("/posts/{id}", tags=['POST'])
```

- Return Valid Status code if an object is not found.
    - Quarkey approach:
```python
@app.get("/posts/{id}", tags=['POST'])
async def get_post(id:int, response: Response):
    """Return Single Posts"""
    for p in my_posts:
        if p['id'] == id:
            return {"data" : p}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message" : f"Post with ID: {id} Not Found"}

```

- Instead a better approach:
    - import ```HTTPException``` from the fastapi module
    - ```raise HTTPException``` with related status code and detail message.
```py
from fastapi import FastAPI, status, HTTPException

@app.get("/posts/{id}", tags=['POST'])
async def get_post(id: int):
    """Return Single Post"""
    for p in my_posts:
        if p['id'] == id:
            return {"data": p}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} Not Found")
```
