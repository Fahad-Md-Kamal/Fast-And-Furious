from typing import Optional

from pydantic import BaseModel

class UserProfile(BaseModel):
    nickname: str
    location: Optional[str] = None
    subscribed_newsletter: bool=True


user = UserProfile(nickname='Fahad')
print(user)

