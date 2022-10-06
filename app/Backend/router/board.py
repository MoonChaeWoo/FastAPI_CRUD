from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from Backend.common.config import conf
from typing import List
from fastapi import Depends
from Backend.database import schemas
from Backend.database.crud import items_crud, users_crud
from sqlmodel import Session
from Backend.database.conn import SessionLocal
from datetime import datetime

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

@router.get("/board", response_class=HTMLResponse, response_model=List[schemas.Item])
# request : Request를 받아야 html 호출 가능
def index(request : Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = items_crud.get_items(db, skip=skip, limit=limit)
    
    context = {
        'request' : request,
        'items' : items,
        'date' : now.strftime('%Y-%m-%d %H:%M:%S')
    }
    return board.TemplateResponse('board_main.html', context)

@router.get("/board/write", response_class=HTMLResponse)
def index(request : Request):
    context = {
        'request' : request,
    }
    return board.TemplateResponse('insertBoard.html', context)

@router.get("/board/about", response_class=HTMLResponse)
def index(request : Request):
    context = {
        'request' : request,
    }
    return board.TemplateResponse('about.html', context)

@router.get("/board/contact", response_class=HTMLResponse)
def index(request : Request):
    context = {
        'request' : request,
    }
    return board.TemplateResponse('contact.html', context)

@router.get("/board/post", response_class=HTMLResponse)
def index(request : Request):
    context = {
        'request' : request,
    }
    return board.TemplateResponse('post.html', context)