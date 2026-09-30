from pydantic import BaseModel

class UserNexus(BaseModel):
    username: str
    password: str
