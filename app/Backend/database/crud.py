# 데이터 읽기
# Session를 sqlalchemy.orm사용하면 db매개변수의 유형을 선언하고 함수에서 더 나은 유형 검사 및 완성 기능을 사용할 수 있다.
# 가져오기 models(SQLAlchemy 모델) 및 schemas(Pydantic 모델 /스키마).

from sqlalchemy.orm import Session
from . import models, schemas

# 유저 한명 가져오기 
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 유저 이메일 가져오기
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 유저 전체 가져오기
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
    
# 데이터 생성
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"

    #데이터로 SQLAlchemy 모델 인스턴스 를 만듭니다.
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # add해당 인스턴스 개체를 데이터베이스 세션에 추가합니다.
    db.add(db_user)
    # commit데이터베이스에 대한 변경 사항(저장되도록).
    db.commit()
    # refresh인스턴스(생성된 ID와 같은 데이터베이스의 새 데이터가 포함되도록)
    db.refresh(db_user)
    return db_user

# item 전체 가져오기
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# 데이터 생성
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item