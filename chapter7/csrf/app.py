from typing import cast
from fastapi import FastAPI, status, HTTPException, Depends, Response, Form
from tortoise.exceptions import IntegrityError, DoesNotExist
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import APIKeyCookie
from tortoise.contrib.fastapi import register_tortoise
from tortoise import timezone
from chapter7.csrf.authentication import authenticate, create_access_token

from chapter7.csrf.models import (
    AccessTokenTortoise,
    UserCreate,
    User,
    UserDB,
    UserTortoise
)
from chapter7.csrf.password import get_password_hash


app = FastAPI()


TOKEN_COOKIE_NAME = "token"
CSRF_TOKEN_SECRET = "FMK_COOKIE_SECREAT"

async def get_current_user(
    token: str = Depends(APIKeyCookie(name=TOKEN_COOKIE_NAME)),
) -> UserTortoise:
    try:
        access_token: AccessTokenTortoise = await AccessTokenTortoise.get(
            access_token=token, expiration_date__gte=timezone.now()
        ).prefetch_related("user")
        return cast(UserTortoise, access_token.user)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


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

@app.post("/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...)):
    user = await authenticate(email, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = await create_access_token(user)

    response.set_cookie(
        TOKEN_COOKIE_NAME,
        token.access_token,
        max_age=token.max_age(),
        secure=True,
        httponly=True,
        samesite="lax",
    )

@app.post("/token")
async def create_token(form_data:OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    email = form_data.username
    password = form_data.password
    user = await authenticate(email, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    token = await create_access_token(user)

    return {"access_token": token.access_token, "token_type": "bearer"}

@app.get("/protected-route", response_model=User)
async def protected_route(user: UserDB = Depends(get_current_user)):
    return User.from_orm(user)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://chapter7_csrf.db"},
    "apps": {
        "models": {
            "models": ["chapter7.csrf.models"],
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