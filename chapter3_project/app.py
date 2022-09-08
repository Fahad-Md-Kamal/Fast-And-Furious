from fastapi import FastAPI

from chapter3_project.routers import posts, users 

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
