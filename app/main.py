from http.client import responses
from multiprocessing import context
from urllib.request import Request
from fastapi import FastAPI
from Backend.common.config import conf
from typing import Optional
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

def create_app():
    # 앱 생성
    
    
    app = FastAPI()

    # 데이터 베이스 이니셜라이즈

    # 레디스 이니셜라이즈

    # 미들웨어 정의

    # 라우터 정의
    
    return app

app = create_app()
config = conf()
templates = Jinja2Templates(directory=config.TEMPLATES)

@app.get("/", response_class=HTMLResponse)
# request : Request를 받아야 html 호출 가능
def index(request : Request):
    context = {
        'request' : request,
        'value_1' : 'request_testValue'
    }
    return templates.TemplateResponse('base.html', context)

if __name__ =="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)