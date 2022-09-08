from pydantic import BaseModel, validator


class Model(BaseModel):
    values: list[int]

    @validator("values", pre=True)
    def split_string_values(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v

p = Model(values="1,2,3,4")
print(p.values)