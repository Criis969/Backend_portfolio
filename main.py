from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from db.client import projects_collection, users_collection
from db.models.users import User, UserDB
from db.models.projects import Project
from bson.objectid import ObjectId
import pydantic
from fastapi.middleware.cors import CORSMiddleware

SECRET_KEY = "688904a521337fdf3c68c477c9a497068d6eeac2fb03b411a197a918aa2163b2"
ALGORITHM = "HS256"
EXPIRATION_TIME = 20


oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

#password @prueba1 $2a$12$8nzRR5U.raL.uxMZ.iwxEOHn0RNnRpRt6tOQRyQYRUTr/qXhK1TWa

async def authenticate_user(user: UserDB):
    user_db = users_collection.find_one({"username": user.username})
    if not user_db:
        return False
    if not pwd_context.verify(user.password,user_db["password"]):
        return False
    expiration = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    token = jwt.encode(
        {"sub": user.username, "exp": expiration},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}
        

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Web page"}

@app.get("/projects")
async def get_projects():
    projects_list = []
    for document in projects_collection.find():
        projects_list.append(document)
    return projects_list

@app.get("/projects/{id_project}")
async def get_project(id_project: str):
    project = projects_collection.find_one({"_id": ObjectId(oid=id_project)})
    return project

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = await authenticate_user(UserDB(username=username,password=password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@app.post("/project")
async def add_project(project: Project, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        try:
            projects_collection.insert_one(project.__dict__)
            return project
        except:
            raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error with database service",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
