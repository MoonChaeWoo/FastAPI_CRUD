import email
from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List
from Backend.database import schemas
from Backend.database.crud import users_crud
from sqlmodel import Session
from Backend.database.conn import SessionLocal
from Backend.common.config import conf
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

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

config = conf()
templates = Jinja2Templates(directory=config.TEMPLATES)

@router.get("/register/", response_class=HTMLResponse, tags=["users"])
def index(request : Request):
    context = {
        'request' : request,
    }
    return templates.TemplateResponse('register.html', context)

# 유저 생성하기
@router.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    db_user = users_crud.get_user_by_email(db, email=user.email)
    print(f'user_db {db_user}')
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_crud.create_user(db=db, user=user)

# 반환하는 값은 SQLAlchemy 모델 또는 SQLAlchemy 모델 목록입니다.
# 그러나 모든 경로 작업 에는 를 response_model사용하는 Pydantic 모델 /스키마 orm_mode가 있으므로
# Pydantic 모델에 선언된 데이터는 모든 일반 필터링 및 유효성 검사와 함께 해당 모델에서 추출되어 클라이언트로 반환됩니다.

# response_models_List[schemas.Item]
# 그러나 그 내용/매개변수는 List가 있는 Pydantic 모델 이므로 데이터가 검색 되어 
# orm_mode문제 없이 정상적으로 클라이언트에 반환됩니다.

# !!! SQLAlchemy는 await다음과 같이 직접 사용할 수 있는 호환성이 없다.
# tags=["users"]는 docs에 users라는 tag가 생긴다.
# 모든 유저 목록 가져오기
@router.get("/users/", response_model=List[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_crud.get_users(db, skip=skip, limit=limit)
    print("----")
    # db에서 온 값을 터미널로 확인하려면 iterator 객체이기 때문에 for로 뽑아서 읽어준다.
    for result in users:
        print(f"id:{result.id} email:{result.email}")
    print("----")
    return users

# 특정 유저 찾기
@router.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 유저 업데이트
@router.post("/users/update", response_model=schemas.User, tags=["users"])
def update_user(user : schemas.userUpdate, db : Session = Depends(get_db)):
    db_user = users_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_crud.update_user(db=db, user=user)


