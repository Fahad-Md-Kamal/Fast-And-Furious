from pydantic import BaseModel

class Parson(BaseModel):
    first_name: str
    last_name: str
    age: int


res = {"first_name": 'Fahad', "last_name": 2345678, "age": '30'}

person = Parson(**res)

print(person)
