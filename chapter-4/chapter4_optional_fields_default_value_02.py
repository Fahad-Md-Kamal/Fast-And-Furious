import time
from datetime import datetime

from pydantic import BaseModel

class Model(BaseModel):
    d: datetime=datetime.now()


o1 =Model()
print(o1.d)

time.sleep(1)

o2 =Model()
print(o2.d)

print(o1.d < o2.d)

