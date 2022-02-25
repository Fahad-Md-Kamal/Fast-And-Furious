## FastAPI Blog App Dev Documentation
<hr>
<br>
<br>

## Part - One [Brows Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/885189adc7e261a41a52b3f600ca8c9c71d7c203)
<hr> 

### GET & POST
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
<br>
<br>
<br>

## Part - Two [Brows Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/ce621b2924ed8854e747c504dacbaf272642f795)
<hr>

### Stractured Data
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
<br>
<br>
<br>

## Part - Three [Brows File](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/ba3ea47820f3509700574dfa691a04262a0d1a8a)
<hr>

### Related API Status Code
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

**This comes first.**
```python
@app.get("/posts/latest", tags=['POST'])
```
**This comes later**


```python
@app.get("/posts/{id}", tags=['POST'])
```
*So that dynamic ```id``` is not replaced by ```latest``` value from the URL.*

<br>
<br>

### Return Valid Status code if an object is not found.

**Quarkey approach:**
```python
from fastapi import FastAPI, Response, status

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

**Preffered Approach**
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
<br>
<br>
<br>

## Part - Four [Brows File](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/5aee14e85069e49b0af141527e5bd24bcda722aa)
<hr>

### Delete Item
- Receive item ```ID``` to be deleted.
- Check if item exist in the data set.
- If exist delete it and send ```204``` status code.
- Else raise ```HTTPException``` error.
- To send related status code add ```status_code=status.HTTP_204_NO_CONTENT``` to the url decorator.

```python

def find_post_index(id: int):
    """Return Index of the Matching post item."""
    for idx, val in enumerate(my_posts):
        if val['id'] == id:
            return idx

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['POST'])
async def delete_post(id: int):
    """ Delete Post With The Given Id"""
    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not-Found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```
<br>
<br>
<br>

### Update Item
- Receive Item ```id``` to be updated
- Check if the item exists.
- If exists get the index of the item.
- Convert the payload data to dict.
- Assign the given ID to the dict.
- Replace the Item to the index position of the list.


```python
def find_post_index(id: int):
    """Return Index of the Matching post item."""
    for idx, val in enumerate(my_posts):
        if val['id'] == id:
            return idx

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
async def update_post(id: int, post: Post):
    """Update a Post with the payload"""
    index = find_post_index(id) 
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not-Found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": post_dict}
```
<br>
<br>
<br>

## Part Five [Brows File](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/dcabb1c3a94af04b345d9e480a800655b06cde1a) 
<hr>

### Re-stracture Project Tree
- Move The ```main.py``` file into the app folder.
- In order to declare the app diractory as a module add an ```__init__.py```

**To Run the Project now, Type**
```bash
uvicorn app.main:app --reload
```

### Connect to the database (e.g: PostGres)
Install the Postgres Package
```bash
pip install psycopg2
```

- Import ```psycopg2``` for database connection.
- Import ```RealDictCursor``` from ```psycopg2.extras``` to show the datafield as python dictionary
- Connect to the database using while loop so that until the db is connected you can run the loop after a certain period.
- User the ```sleep()``` function to loop connection if fails after a certain period.
```py
import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_db', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        print("database Connection was successfull")
        cursor = conn.cursor()
        break
    except Exception as error:
        print("database Connection was Faild")
        print("Error", error)
        time.sleep(2)
```

### Make Database Call from within API functions
 - User the connection cursor to exectue SQL schemas.
 - To Make database call, it is required to call fetchall() method.
```py
@app.get("/posts", tags=['POST'])
async def get_posts():
    """Return All Posts"""
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

```
