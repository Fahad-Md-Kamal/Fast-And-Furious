from fastapi import FastAPI, Body, status, HTTPException

app = FastAPI()


@app.post('/password')
async def check_password(password: str = Body(...), password_confirm: str = Body(...)):
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Passwords didn\'t matched.'
        )
    return {"message": "Hurrah! Password Matched."}
