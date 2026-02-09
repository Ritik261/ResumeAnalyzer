from fastapi import APIRouter, Request, Depends, HTTPException, Response, Cookie
from app.auth.auth import hash_password, verify_password, create_access_token,SECRET_KEY,ALGORITHM
from sqlalchemy.orm import Session
from app.database.database import get_db
from pydantic import BaseModel
from jose import jwt, JWTError
from dotenv import load_dotenv
from app.model.usermodel import User

load_dotenv()
router = APIRouter(prefix="/v1")

class UserQuery(BaseModel):
    query: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def get_current_user(access_token:str = Cookie(None),db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Token not valid")
    return {"message": "logged in"}
    # curr_token = request.cookies.get("access_token")

    # print("access token", curr_token)
    # if not token:
    #     raise HTTPException(status_code=401, detail="Not logged in")
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, ALGORITHM )
    #     userEmail: str = payload.get("sub")
    #     if userEmail is None:
    #         raise HTTPException(status_code=401, detail="Invalid Token") 
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Invalid Token")

    # user =  db.query(User).filter(User.email == userEmail).first()
    # if user is None:
    #     raise HTTPException(status_code=401, detail="user not found")
    # return user

@router.get("/")
def routecheck():
    return {"message": "route working"}

@router.post("/post")
def hello(request: UserQuery, user = Depends(get_current_user)):
    #return {"Mesaage": f"{user}and{request.query}"}
    return {"message": f"{request}"}

@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user already exists")
    hashed_password = hash_password(user.password)
    new_user = User(username = user.username, email= user.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user registered success ✅"}

@router.post("/login")
async def login(user: UserLogin, response: Response,db: Session=Depends(get_db)):
    dbuser = db.query(User).filter(User.email == user.email).first()

    if not dbuser or not verify_password(user.password, dbuser.password):
        raise HTTPException(status_code=401,detail="Invalid Credentials" )

    # if(user.password != dbuser.password):
    #     raise HTTPException(status_code=401, detail="Invalid Credentials")
    # return{"message": "user logged in 👍"}

    token = create_access_token(data={"sub":dbuser.email})

    print("Token Generated",token)

    response.set_cookie(
        key="access_token",
        value=f"Bearer{token}",
        httponly=True,
        max_age=3600,
        samesite="lax"
    )

    return {"message": f"login success, welcome {dbuser.username}"}