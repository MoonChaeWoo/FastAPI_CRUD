from fastapi import APIRouter, Depends, Cookie, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from Backend.common.config import conf
from typing import List
from Backend.database import schemas
from Backend.database.crud import items_crud, users_crud
from sqlmodel import Session
from Backend.database.conn import SessionLocal
from datetime import datetime
from jose import jwt
from Backend.router.login import SECRET_KEY

router = APIRouter()

config = conf()
board = Jinja2Templates(directory=config.BOARD)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

now = datetime.now()

@router.get("/board", response_class=HTMLResponse, response_model=List[schemas.Item], tags=["board"])
# request : Request를 받아야 html 호출 가능
def index(request : Request, skip: int = 0, limit: int = 100, access_token : str | None = Cookie(default=None), db: Session = Depends(get_db)):
    # access_token : str | None = Cookie(default=None)
    # 쿠키를 받아오려면 웹에 저장된 쿠키의 이름과 파라미터의 이름을 동일 시 해야만 값이 불러와진다.
    items = items_crud.get_items(db, skip=skip, limit=limit)
    token_ckeck(access_token, db)
    context = {
        'request' : request,
        'items' : items,
    }
    return board.TemplateResponse('board_main.html', context)

@router.get("/board/write", response_class=HTMLResponse, tags=["board"])
def index(request : Request, access_token : str | None = Cookie(default=None), db: Session = Depends(get_db)):
    # access_token : str | None = Cookie(default=None)
    # 쿠키를 받아오려면 웹에 저장된 쿠키의 이름과 파라미터의 이름을 동일 시 해야만 값이 불러와진다.
    token_ckeck(access_token, db)
    context = {
        'request' : request,
    }
    return board.TemplateResponse('insertBoard.html', context)

@router.get("/board/about", response_class=HTMLResponse, tags=["board"])
def index(request : Request, access_token : str | None = Cookie(default=None), db: Session = Depends(get_db)):
    # access_token : str | None = Cookie(default=None)
    # 쿠키를 받아오려면 웹에 저장된 쿠키의 이름과 파라미터의 이름을 동일 시 해야만 값이 불러와진다.
    token_ckeck(access_token, db)
    context = {
        'request' : request,
    }
    return board.TemplateResponse('about.html', context)

@router.get("/board/contact", response_class=HTMLResponse, tags=["board"])
def index(request : Request, access_token : str | None = Cookie(default=None), db: Session = Depends(get_db)):
    # access_token : str | None = Cookie(default=None)
    # 쿠키를 받아오려면 웹에 저장된 쿠키의 이름과 파라미터의 이름을 동일 시 해야만 값이 불러와진다.
    token_ckeck(access_token, db)
    context = {
        'request' : request,
    }
    return board.TemplateResponse('contact.html', context)

@router.get("/board/post/{post_id}", response_class=HTMLResponse, response_model=schemas.Item, tags=["board"])
def index(request : Request, post_id: int, access_token : str | None = Cookie(default=None), db: Session = Depends(get_db)):
    # access_token : str | None = Cookie(default=None)
    # 쿠키를 받아오려면 웹에 저장된 쿠키의 이름과 파라미터의 이름을 동일 시 해야만 값이 불러와진다.
    token_ckeck(access_token, db)
    item = items_crud.read_user_item(db, post_id)
    context = {
        'request' : request,
        'item' : item
    }
    return board.TemplateResponse('post.html', context)

    # 토큰이 유무 체크 
def token_ckeck(value, db):

    if not value:
        raise HTTPException(status_code=401, detail="Inactive user")

    try:
        decode = jwt.decode(value, SECRET_KEY)
    except:
        raise HTTPException(status_code=500, detail="An authentication error occurred")

    user_email = decode['sub']

    if not users_crud.get_user_by_email(db, user_email):
        return RedirectResponse("/", status_code=403)
    return user_email