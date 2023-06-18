from fastapi import FastAPI
from pydantic import BaseModel


class Project(BaseModel):
    id: int
    name: str
    owner: str
    link: str
    description: str

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Web page"}

@app.get("/projects")
async def get_projects():
    list_projects=[Project(id=0,name="Test project 1",owner="Cristian",link="http://project1.com",description="It is the test project 1"),
                   Project(id=1,name="Test project 2",owner="Cristian",link="http://project2.com",description="It is the test project 2"),
                   Project(id=2,name="Test project 3",owner="Cristian",link="http://project3.com",description="It is the test project 3")]
    return list_projects

@app.get("/projects/{id_project}")
async def get_project():
    project = Project(id=0,name="Test project",owner="Cristian",link="http://project.com",description="It is a test project")
    return project