from pydantic import BaseModel

class Project(BaseModel):
    name: str
    owner: str
    link: str
    description: str