from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Web page"}

@app.get("/projects")
async def get_projects():
    return {"message": "Return projects list"}

@app.get("/projects/{id_project}")
async def get_project():
    return {"message": "Return a project"}