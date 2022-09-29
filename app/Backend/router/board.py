from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from Backend.common.config import conf

router = APIRouter()

config = conf()
board = Jinja2Templates(directory=config.BOARD)

@router.get("/board", response_class=HTMLResponse)
# request : Request를 받아야 html 호출 가능
def index(request : Request):
    context = {
        'request' : request,
    }
    return board.TemplateResponse('board_main.html', context)

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