# 데이터 읽기
# Session를 sqlalchemy.orm사용하면 db매개변수의 유형을 선언하고 함수에서 더 나은 유형 검사 및 완성 기능을 사용할 수 있다.
# 가져오기 models(SQLAlchemy 모델) 및 schemas(Pydantic 모델 /스키마).

from sqlalchemy.orm import Session
from .. import models, schemas

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