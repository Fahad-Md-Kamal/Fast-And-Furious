from fastapi import FastAPI

from .config import Settings
from .routers import post, user, auth, vote

from . import models
from .database import engine

settings = Settings()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
