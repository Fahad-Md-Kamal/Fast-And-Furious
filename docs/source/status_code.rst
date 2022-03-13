=======================
Related API Status Code
========================

`Part - Three <https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/ba3ea47820f3509700574dfa691a04262a0d1a8a>`_

Import status package from fastapi module
add ``status_code=status.HTTP_201_CREATED`` to the url decorator.

.. code-block:: python
    :emphasize-lines: 3,5

    from fastapi import FastAPI, status

    @app.post("/posts", status_code=status.HTTP_201_CREATED, tags=['POST'])
    async def create_post(post: Post):
        """Create Posts"""
        post_dict = post.dict()
        post_dict['id'] = randrange(0, 9999999)
        my_posts.append(post_dict)
        return {"data": my_posts}

Place the urls in perfect order hierarchy so that dynamic values do not replace an actual value of the request.

**This comes first.**

.. code-block:: python
    :emphasize-lines: 1,1

    @app.get("/posts/latest", tags=['POST'])

**This comes later**


.. code-block:: python
    :emphasize-lines: 1,1

    @app.get("/posts/{id}", tags=['POST'])

So that dynamic ``id`` is not replaced by ``latest`` value from the URL.


Return Valid Status code if an object is not found
----------------------------------------------------

**Quarkey approach:**

.. code-block:: python
    :emphasize-lines: 1,11

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

**Preffered Approach** |
Import ``HTTPException`` from the fastapi module
``raise HTTPException`` with related status code and detail message.

.. code-block:: python
    :emphasize-lines: 1,11

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
