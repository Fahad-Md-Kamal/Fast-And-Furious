from datetime import date
from pydantic import BaseModel, validator


class Person(BaseModel):
    first_name: str
    last_name: str
    birthdate: date

    @validator('birthdate')
    def validate_birthdate(cls, v: date):
        delta = date.today() - v
        age =delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v

p = Person(first_name='Fahad', last_name='Md Kamal', birthdate='1900-01-01')
print(p)