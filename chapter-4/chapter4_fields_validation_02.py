from datetime import datetime
import time

from pydantic import BaseModel, Field


def list_factory():
    return ["a", "b", "c", "d"]

class Model(BaseModel):
    l: list[str] = Field(default_factory=list_factory)
    d: str = Field(default_factory=datetime.now)
    l2: list[str] = Field(default_factory=list)


m = Model()
print(m)
time.sleep(1)
m2 = Model()
print(m2)
print(m2.d == m.d)