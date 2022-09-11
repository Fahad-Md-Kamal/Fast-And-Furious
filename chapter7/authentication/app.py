from fastapi import FastAPI, status, HTTPException
from tortoise.exceptions import IntegrityError
from tortoise.contrib.fastapi import register_tortoise

from chapter7.authentication.models import (
    UserCreate,
    User,
    UserDB,
    UserTortoise
)
from chapter7.authentication.password import get_password_hash


app = FastAPI()


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)

    try:
        user_tortoise = await UserTortoise.create(
            **user.dict(), hashed_password=hashed_password
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email Already Exists')

    return User.from_orm(user_tortoise)



TORTOISE_ORM = {
    "connections": {"default": "sqlite://chapter7_authentication.db"},
    "apps": {
        "models": {
            "models": ["chapter7.authentication.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)