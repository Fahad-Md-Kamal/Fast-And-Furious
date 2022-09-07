from fastapi import FastAPI, Query

app = FastAPI()


@app.get('/users')
async def get_user(page: int = Query(1, gt=1), size: int = Query(10, le=100)):
    return {"page" : page, "size" : size}

# ------------------------------------------------------------------------------
# from enum import Enum
# class UsersFormat(str, Enum):
#     SHORT = 'short'
#     FULL = 'full'

# @app.get('/users')
# async def get_user(format: UsersFormat, page: int =1, size: int = 10, ):
#     return {"format" : format, "page" : page, "size" : size}


# ------------------------------------------------------------------------------
# @app.get('/users')
# async def get_user(page: int =1, size: int = 10):
#     return {"page" : page, "size" : size}


