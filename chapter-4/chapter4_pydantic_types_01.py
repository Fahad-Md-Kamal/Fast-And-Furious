from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError

class User(BaseModel):
    email : EmailStr
    website : HttpUrl

# Invalid Email
try:
    User(email='fahad', website='https://fahadmdkamal@gmail.com')
except ValidationError as e:
    print(str(e))

print(' - '*10)
# Invalid Url
try:
    User(email='fahadmdkamal@gmail.com', website='fahadmdkamal@gmail.com')
except ValidationError as e:
    print(str(e))

print(' - '*10)
#Valid Object
user = User(email='fahadmdkamal@gmail.com', website='https://fahadmdkamal.com')

print(user)