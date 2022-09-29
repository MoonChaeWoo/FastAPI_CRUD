from urllib.request import Request
from fastapi import FastAPI
from Backend.common.config import conf
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from Backend.database import models
from Backend.database.conn import engin
from Backend.router import board, items, users, dashboard
import time
from Backend.api.airInfo_json import json_list

def create_app():
    # 앱 생성
    app = FastAPI(
        title="FastAPI CRUD",
        description="FastAPI CRUD Project"
    )

    # 데이터 베이스 이니셜라이즈
    models.Base.metadata.create_all(bind=engin)

    # 레디스 이니셜라이즈

    # 미들웨어 정의
    # request는 실제 request로 API로 보내진 정보를 담고있다.
    # call_next는 함수 파라메터로, API 리퀘스트를 API에 해당되는 path에 보내고, response를 리턴하는 역할을 하는 파라메터이다.
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # 라우터 정의
    app.include_router(board.router)
    app.include_router(users.router)
    app.include_router(items.router)
    app.include_router(dashboard.router)

    return app

app = create_app()

config = conf()
templates = Jinja2Templates(directory=config.TEMPLATES)

app.mount("/static", StaticFiles(directory=config.STATIC), name="static")

@app.get("/", response_class=HTMLResponse)
# request : Request를 받아야 html 호출 가능
def index(request : Request):
    # 'context must include a "request" key' 이기에 넣어야한다.
    context = {
        'request' : request,
    }
    return templates.TemplateResponse('main.html', context)

if __name__ =="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

# 번외 
# startup이벤트
# 응용 프로그램이 시작되기 전에 실행되어야 하는 함수를 추가하려면 이벤트로 선언한다.
# @app.on_event("startup")
# async def startup():
#     pass
# shutdown이벤트
# 애플리케이션이 종료될 때 실행되어야 하는 함수를 추가하려면 이벤트로 선언
# @app.on_event("shutdown")
# async def shutdown():
#     pass