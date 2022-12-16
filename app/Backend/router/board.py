from fastapi import APIRouter, Depends, Cookie, Request, HTTPException, status, UploadFile
from pathlib import Path
from os import path
import os
import aiofiles, asyncio
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
uploadPath = config.UPLOAD

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

@router.post("/board/write", response_class=HTMLResponse, tags=["board"])
async def index(request : Request, form_data : schemas.ItemCreate = Depends(schemas.ItemCreate.as_form), access_token : str | None = Cookie(default=None), db : Session = Depends(get_db)):
    # access_token : str | None = Cookie(default=None)
    # 쿠키를 받아오려면 웹에 저장된 쿠키의 이름과 파라미터의 이름을 동일 시 해야만 값이 불러와진다.
    user_info = token_ckeck(access_token, db)

    if form_data.uploadFile != None:
        filePath = save_upload_file(form_data.uploadFile, user_info["email"])
        form_data.uploadFile = bytes(filePath, encoding='utf-8')
        items_crud.create_user_item(db, form_data, user_info["id"])
        # UploadFile안의 속성
        # 1. filename
        # 2. content_type
        # 3. file
        # print(f'path ========================>>> {form_data.uploadFile.decode("utf-8")}')
    else:
        items_crud.create_user_item(db, form_data, user_info["id"])

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
    try:
        decode = jwt.decode(value, SECRET_KEY)
    except:
        raise HTTPException(status_code=500, detail="An authentication error occurred")
        
    user_email = decode['sub']

    id : int = 0
    if not users_crud.get_user_by_email(db, user_email):
        raise HTTPException(status_code=403, detail="An authentication error occurred")
    else:
        id = users_crud.get_user_by_email(db, user_email).id

    user_info = {'email' : user_email, 'id' : id}
    return user_info

def mkdir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error : fail mkdir')

def save_upload_file(uploadFile : UploadFile, user_email : str) -> str:

    yearDir = path.join(uploadPath, str(datetime.today().year))
    monDir = path.join(yearDir, str(datetime.today().month))
    dayDir = path.join(monDir, str(datetime.today().day))
    userDir = path.join(dayDir, str(user_email))
    # 파일은 통째로 저장하는거 보단 연도, 날짜 등으로 나눠 저장하는게 성능에 더 좋다.
    for i in uploadPath, yearDir, monDir, dayDir, userDir:
        mkdir(i)

    filePath = path.join(userDir, uploadFile.filename)

    CHUNK_SIZE = 1024
    with open(filePath, 'wb') as buffer:
        while contents := uploadFile.file.read(CHUNK_SIZE):
            buffer.write(contents)
        uploadFile.file.close()
    return filePath

# with를 함께 사용한다면 파일 입출력 단계에서 해당 파일을 위해 openk close를 해주어야하는데 
# "with open('C:/pythonTest/abc.txt', 'r') as file_data" 를 한다면 with가 자동으로 close를 불러와준다.