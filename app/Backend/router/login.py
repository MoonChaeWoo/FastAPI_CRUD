import email
from typing import List
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, APIRouter, status
from Backend.database import schemas
from Backend.database.crud import users_crud
from sqlmodel import Session
from Backend.common.config import conf
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from Backend.database.conn import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt # pip install "python-jose[cryptography]
from os import environ
from dotenv import load_dotenv
# .env 환경파일 로드 
load_dotenv()

# apiKey : 어플리케이션을 특정하게 하는 키. 쿼리, 헤더, 쿠키에서 얻어온다
# http : http authenication 시스템이다. 하기 내용을 포함한다
#   -  bearer : Bearer값과 토큰을 포함하고 있는 Autorization 헤더이다. OAuth2를 상속한다
#   -  HTTP 기반 authentication이다
#   -  HTTP digest 인증기법 이용한다
# oauth2 : 모든 OAuth2 security에 관한 내용을 다룬다. 이를 flow라고 한다
# openIdConnect : OAuth2 인증데이터를 자동으로 찾아준다.

router = APIRouter()

config = conf()
templates = Jinja2Templates(directory=config.TEMPLATES)

# Dependency
# 디펜던시에서 배웠던 디펜던시 + yield 조합을 통하여 리퀘스트에서 db세션을 생성하고 리스폰스시에 db를 종료하도록 코드를 작성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# oauth2_scheme variable은 객체이지만 callbale이다. 
# 즉 Depends에 사용이 가능하다!
# ex) async def read_items(token: str = Depends(oauth2_scheme)):
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

SECRET_KEY = environ['SECRET_KEY']
ALGORITHM = environ['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = environ['ACCESS_TOKEN_EXPIRE_MINUTES']

@router.get("/login/", response_class=HTMLResponse, tags=["login"])
def index(request : Request):
    context = {
        'request' : request,
    }
    return templates.TemplateResponse('login.html', context)

@router.post("/login/token", response_model=schemas.Token, tags=["login"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=400, detail="Email and password must be provided")
    user_auth = users_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": user_auth.email}, expires_delta=access_token_expires
        )
        # users_crud에 구현해둔 해쉬 비밀번호 비교를 이용함
        return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_crud.get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(status_code=400, detail="Inactive user")

@router.get("/users/me/", response_model=schemas.User, tags=["login"])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/", tags=["login"])
async def read_own_items(current_user: schemas.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
