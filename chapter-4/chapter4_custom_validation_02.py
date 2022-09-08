from pydantic import BaseModel, EmailStr, root_validator


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @root_validator()
    def password_match(cls, values):
        password = values.get("password")
        password_confirmation= values.get("password_confirmation")
        if password != password_confirmation:
            raise ValueError("Passwords don't match")
        return values

p = UserRegistration(email='fahadmdkamal@gmail.com', password='1234',password_confirmation='123456789')
print(p)