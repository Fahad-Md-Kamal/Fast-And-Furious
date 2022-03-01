## FastAPI Blog App Dev Documentation
<br>
<br>

## Part - One [Brows Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/885189adc7e261a41a52b3f600ca8c9c71d7c203)

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

## Part - Two [Brows Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/ce621b2924ed8854e747c504dacbaf272642f795)

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
    published: bool = True
    rating: Optional[int] = None

@app.post("/create-post", tags=['POST'])
async def create_post(post:Post):
    print(post.dict())
    return {"data":"Post Created Successfully"}  
```
<br>

## Part - Three [Brows File](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/ba3ea47820f3509700574dfa691a04262a0d1a8a)
<br>

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

## Part - Four [Brows File](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/5aee14e85069e49b0af141527e5bd24bcda722aa)

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

## Part Five [Brows File](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/dcabb1c3a94af04b345d9e480a800655b06cde1a) 

### Re-stracture Project Tree
- Move The ```main.py``` file into the app folder.
- In order to declare the app diractory as a module add an ```__init__.py```

**To Run the Project now, Type**
```bash
uvicorn app.main:app --reload
```
<br>

### Connect to the database (e.g: PostgreSQL)
Install the Postgres Package
```bash
pip install psycopg2
```

- Import ```psycopg2``` for database connection.
- Import ```RealDictCursor``` from ```psycopg2.extras``` to show the datafield as python dictionary
- Connect to the database using while loop so that until the db is connected you can run the loop after a certain period.
- User the ```sleep()``` function to loop connection if fails after a certain period.
<br>

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
 - To Make database call, it is required to call ```fetchall()``` method.
```py
@app.get("/posts", tags=['POST'])
async def get_posts():
    """Return All Posts"""
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

```
### Get Single Post
- Alwasy pass user's inputs ```str(id)``` as SQL variable ```%s``` in order to avoid sql injection.
- Make ```cursor``` to call on database by ```cursor.fetchone()```.
```python
@app.get("/posts/{id}", tags=['POST'])
async def get_post(id: int):
    """Return Single Post"""

    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),))
    post = cursor.fetchone()

    if post:
        return {"data": post}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post Not-Found"
        )
```

### Create schema
- Write ```INSERT``` SQL schema that needs to be created
- Add ```RETURNING *``` with the SQL schema to return the whole object once it is created.
- Remember to Commit changes to the database (N.B: Without ```conn.commit()``` changes wouldn't be applied to the database.)

```python
@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['POST'])
async def create_post(post: Post):
    """Create Posts"""

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}
```

### Update Schema
- Write update schema with SQL variable fields.
- Call the ```fetchone()``` to make the change.
- Finally apply changes to the database by calling ```commit()```

```python
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
async def update_post(id: int, post: Post):
    """Update a Post with the payload"""

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post Not-Found"
        )

    return {"data": post}
```

### Delete Schema
- Similar to udpated operation but this time ```DELETE``` SQL Schema needs to be passed.

```python
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['POST'])
async def delete_post(id: int):
    """ Delete Post With The Given Id"""

    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post Not-Found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
```
<br>

## Part Six [Brow Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/e7ece9dc533c175223348ad318502ce7060ced28)

### Connect to ORM
- Install sqlalchemy library

```sh
pip install sqlalchemy
```

- Create ```database.py``` file that will be responsible for connecting our project to the database engine.
- Provide SQL database url ```'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'```
- Pass the user to ```create_engine()``` function
- Now create a session with the engin as bind parameter ```sessionmaker(autocommit=False, autoflush=False, bind=engine)```
- Make a ```Base``` variable from ```declarative_base()``` since it will be inherited to create all the models of the project.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```
<br>

### Connect database engine to FastApi
- Create a function at ```database.py``` file called ```get_db()```
- Create database session using the ```SessionLocal``` variable.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
- Now in ```main.py``` import ```models```, from ```database.py``` import database session name ```engine``` that we have created using ```sessionmaker()``` function and the ```get_db()``` function
- Import ```session``` from ```sqlalchemy.orm```
- Make database tables if not exists by calling the db session (e.g. ```models.Base.metadata.create_all(bind=engine)```) at the beginning of the project

```python
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
```
<br>

### Creating model
- Create a file named ```model.py``` where all the database models will be
- Import ```Base``` from the ```database.py``` since it will be inhearited to all the models
- Import necessary objects from ```sqlalchemy``` library for creating database table.
<br>

```python
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
```

## Part Seven [Brow Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/d208bba4d967fd2f82c3c18052e5a2961cdded46)

### **SqlAlchemy CRUD Operations**
<br>

***Always pass the db session ```db: Session = Depends(get_db)``` to the parameter to the methods that are going to have database operations.***
<br>
<br>

#### Get All Posts
- Generate raw sql schema on Post model using ```db.query(models.Post)```.
- To execute, this needs to be trailed by ```.all()```. **e.g.** ```db.query(models.Post).all()```.

```python
@app.get("/posts", tags=['POST'])
async def get_posts(db: Session = Depends(get_db)):
    """ Return All Posts """
    
    posts = db.query(models.Post).all()
    
    return {"data": posts}
```
<br>

#### Get Single Post Detail
- Make the sql query by using the ```db.query(models.Post)``` and trail it with ```.filter(models.Post.id == id)```.
- Return the first object from the query set result since, the query will return objects list.

```python
@app.get("/posts/{id}", tags=['POST'])
async def get_post(id: int, db: Session = Depends(get_db)):
    """ Return Single Post """
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")
    
    return {"data": post.first()}
```
<br>

#### Create New Post
- Create New post object by mapping each modle field to the post data ```models.Post(title=post.title, content=post.content, published=post.published)```

- A simplification of this tiring process is to convert the post data to a ```dict()``` object and pass it by exploding the dict using **```**```** symbles to the dict object. **e.g.** ```models.Post(**post.dict())```
- Add the post to the database with ```db.add(new_post)```.
- Commit change to the database ```db.commit()```.
- Refresh newly created database object ```db.refresh(new_post)```.

```python
@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['POST'])
async def create_post(post: Post, db: Session = Depends(get_db)):
    """ Create Posts """

    new_post = models.Post(**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data": new_post}
```
<br>

#### Update Post
- First get the post detail, similar to single post detail.
- Now, update the result with the updated_post payload data.
- Add ```synchronize_session=False``` to the queryset **e.g.** ```post_query.update(updated_post.dict(), synchronize_session=False)```.
- Commit changes to the database.
- return the result by executing the generated sql command with ```.first()```.

```python
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['POST'])
async def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    """ Update a Post """
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return {"data": post_query.first()}
```
<br>

#### Delete Post
- Similar to single post detail first get the datbase object with the id.
- Execute ```.delete()``` method.
- Commit change to the database.

```python
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['POST'])
async def delete_post(id: int, db: Session = Depends(get_db)):
    """ Delete Post """
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post Not-Found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```


## Part Eight [Brow Files](https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/)

### Schema Model
- These are the models that inform users about the required input fields of a model.
- Remove the Post Model from the ```main.py``` file to a new file called ```schemas.py```.
- Create a base post model that will be inherited for diffrent purposes. **e.g** (create, update, partial update)
<br>

***N.B:*** Schema Models are similar to Django Forms or Django REST Framework's Serializer Models. They holds the requried user input data fields that the executation requires.
<br>

```python
# /schemas.py

from pydantic import BaseModel

class PostBase(BaseModel):
    """ Responsible for maping Post Object's Data field """
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass
```
<br>

- Now import those to the api functions and use them.

```python
# /main.py

from . import schemas

def create_post(post: schemas.PostCreate):
    """ Create Post """
    ...

def update_post(id: int, updated_post: schemas.PostUpdate):
    """ Update Post """
    ...

```

#### Create Response Model
- Inherit the Base Post Model and add fields that the users could see.

```python
class Post(PostBase):
    """ Responsible for Allowing user's what data they can see """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
```

- Add ```response_model= schemas.Post``` the the url decorator.

```python
@app.put("/posts/{id}", response_model= schemas.Post)
```
<br>
- **N.B.** For List Response like in ```get_all_posts()``` pass it through ```List[]``` imported from typing

```python
@app.get("/posts", response_model= List[schemas.Post])
```