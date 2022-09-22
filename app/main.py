from http.client import responses
from multiprocessing import context
from urllib.request import Request
from fastapi import FastAPI
from Backend.common.config import conf
from typing import Optional, List
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from Backend.database import crud, models, schemas
from Backend.database.conn import SessionLocal, engin
from sqlmodel import Field, Session, SQLModel, create_engine, select

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

    # 라우터 정의
    
    return app

app = create_app()

config = conf()
templates = Jinja2Templates(directory=config.TEMPLATES)
app.mount("/static", StaticFiles(directory=config.STATIC), name="static")

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

@app.get("/", response_class=HTMLResponse)
# request : Request를 받아야 html 호출 가능
def index(request : Request):
    context = {
        'request' : request,
        'value_1' : 'request_testValue'
    }
    return templates.TemplateResponse('main.html', context)


# Dependency
# 디펜던시에서 배웠던 디펜던시 + yield 조합을 통하여 리퀘스트에서 db세션을 생성하고 리스폰스시에 db를 종료하도록 코드를 작성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# schemas.UserCreat : 스키마의 UserCreate 이용
# db : Session = Depends(get_db()) 필요한 종성성을 생성하여 해당 세션을 직접 가져오기
#      이를 통해 crud.get_user 내부에서 직접 호출하고 해당 세션을 사용할 수 있다.
@app.post("/users/", response_model=schemas.User)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# 반환하는 값은 SQLAlchemy 모델 또는 SQLAlchemy 모델 목록입니다.
# 그러나 모든 경로 작업 에는 를 response_model사용하는 Pydantic 모델 /스키마 orm_mode가 있으므로
# Pydantic 모델에 선언된 데이터는 모든 일반 필터링 및 유효성 검사와 함께 해당 모델에서 추출되어 클라이언트로 반환됩니다.

# response_models_List[schemas.Item]
# 그러나 그 내용/매개변수는 List가 있는 Pydantic 모델 이므로 데이터가 검색 되어 
# orm_mode문제 없이 정상적으로 클라이언트에 반환됩니다.

# !!! SQLAlchemy는 await다음과 같이 직접 사용할 수 있는 호환성이 없다.
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    print("----")
    # db에서 온 값을 터미널로 확인하려면 iterator 객체이기 때문에 for로 뽑아서 읽어준다.
    for result in users:
        print(f"id:{result.id} email:{result.email}")
    print("----")
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

if __name__ =="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)