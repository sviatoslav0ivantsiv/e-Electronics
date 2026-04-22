from pydantic import BaseModel

class UserCredentials(BaseModel):
    name: str
    password: str
