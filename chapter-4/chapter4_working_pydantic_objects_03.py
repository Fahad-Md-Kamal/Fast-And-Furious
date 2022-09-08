from datetime import date
from enum import Enum

from pydantic import BaseModel

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"

class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: list[str]
    address: Address

    def name_dict(self):
        return self.dict(include={"first_name", "last_name"})

person = Person(
    first_name="Fahad",
    last_name="Md Kamal",
    gender=Gender.MALE,
    birthdate="1991-01-01",
    interests=["travel", "sports"],
    address={
        "street_address":"1234",
        "postal_code":'14444',
        "city":"dhaka",
        'country': "Bangladesh"
    }
)

dict_person2 = person.name_dict()
print(dict_person2, end='\n\n')