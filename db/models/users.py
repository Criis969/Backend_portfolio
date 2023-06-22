from pydantic import BaseModel

class User(BaseModel):
    username: str

class UserDB(User):
    password: str