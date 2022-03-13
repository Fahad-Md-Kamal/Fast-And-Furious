=======================
Stractured Data
=======================

`Part - Two <https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/ce621b2924ed8854e747c504dacbaf272642f795>`_


* Basic Data Model using Pydentic lib
* Making Optional model field
* Assining Default value to the model fild.

.. code-block:: python
    :emphasize-lines: 7, 15

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
