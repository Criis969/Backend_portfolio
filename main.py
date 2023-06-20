from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "688904a521337fdf3c68c477c9a497068d6eeac2fb03b411a197a918aa2163b2"
ALGORITHM = "HS256"

class Project(BaseModel):
    id: int
    name: str
    owner: str
    link: str
    description: str

class User(BaseModel):
    username: str

class UserDB(User):
    password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#password @prueba1
user_db = UserDB(username="admin",password="$2a$12$8nzRR5U.raL.uxMZ.iwxEOHn0RNnRpRt6tOQRyQYRUTr/qXhK1TWa")

async def authenticate_user(user: UserDB):
    if user.username != user_db.username:
        return False
    if not pwd_context.verify(user.password, user_db.password):
        return False
    expiration = datetime.utcnow() + timedelta(minutes=2)
    token = jwt.encode(
        {"sub": user.username, "exp": expiration},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}
        

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