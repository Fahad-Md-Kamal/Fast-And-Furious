======
Setup
======

`Part - One <https://github.com/Fahad-Md-Kamal/Fast-And-Furious/tree/885189adc7e261a41a52b3f600ca8c9c71d7c203>`_

FastAPI Blog App Dev Documentation
-----------------------------------

Basics of FastAPI
Basic GET and POST request

.. code-block:: python
   :emphasize-lines: 4,6,10

    from fastapi import FastAPI
    from fastapi.params import Body
    
    app = FastAPI()

    @app.get("/", tags=['POST'])
    async def home_view():
        return {"message": "In the name of Allah, I'm beginning"}

    @app.post("/create-post", tags=['POST'])
    async def create_post(payload: dict=Body(...)):
        return {"new_post" : "Post Created Successfully"}
