# 데이터 읽기
# Session를 sqlalchemy.orm사용하면 db매개변수의 유형을 선언하고 함수에서 더 나은 유형 검사 및 완성 기능을 사용할 수 있다.
# 가져오기 models(SQLAlchemy 모델) 및 schemas(Pydantic 모델 /스키마).

from operator import and_
from sqlalchemy.orm import Session
from Backend.database import models, schemas

# item 전체 가져오기
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

# db.users.filter_by(name == 'Joe')
# db.users.filter(db.users.name == 'Joe')
# 위이 2개는 같은 의미이다.
# db.users.filter(or_(db.users.name=='Ryan', db.users.country=='England'))

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item, models.User).filter(models.Item.owner_id == models.User.id).order_by(models.Item.id.desc()).offset(skip).limit(limit).all()
# .order_by()는 필터 바로 다음에 쓰거나 쿼리 바로 뒤에 사용해야 한다. offset이나 limit 뒤에 사용하면 오류 발생함. 

# 데이터 생성 (Create)
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 데이터 읽기 (Read)
def read_user_item(db: Session, post_id : int):
    return db.query(models.Item, models.User).filter(and_(models.Item.owner_id == models.User.id, models.Item.id == post_id)).first()

# 데이터 수정 (Update)
def update_user_item(db: Session, item : schemas.ItemUpdate, user_id: int):
    update_title = item.title
    update_content = item.description

    db.query(models.Item).filter_by(id=item.id, user_id=user_id).update({"title" : update_title, "description" : update_content})
    db.commit()
    return db.query(models.Item).filter_by(id=item.id, user_id=user_id).first()

# 데이터 삭제 (Delete)
def delete_user_item(db: Session, board_id : int):
    db.query(models.Item).filter_by(id=board_id).delete()
    db.commit()