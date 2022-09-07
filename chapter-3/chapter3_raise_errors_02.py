from fastapi import FastAPI, Body, status, HTTPException

app = FastAPI()


@app.post('/password')
async def check_password(password: str = Body(...), password_confirm: str = Body(...)):
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "message":'Passwords didn\'t matched.',
                "hints":[
                    "Check the caps lock on you keyboard",
                    "Try to make the password visible by clicking on the eye icon to check your typing"
                ]
                }
            
        )
    return {"message": "Hurrah! Password Matched."}
