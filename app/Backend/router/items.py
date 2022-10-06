from fastapi import APIRouter
from typing import List
from fastapi import Depends
from Backend.database import schemas
from Backend.database.crud import items_crud
from sqlmodel import Session
from Backend.database.conn import SessionLocal
 
router = APIRouter()

# Dependency
# 디펜던시에서 배웠던 디펜던시 + yield 조합을 통하여 리퀘스트에서 db세션을 생성하고 리스폰스시에 db를 종료하도록 코드를 작성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 게시글 생성
@router.post("/users/{user_id}/items/", response_model=schemas.Item, tags=["items"])
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return items_crud.create_user_item(db=db, item=item, user_id=user_id)

# 게시글 읽기
@router.get("/items/", response_model=List[schemas.Item], tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = items_crud.get_items(db, skip=skip, limit=limit)
    return items