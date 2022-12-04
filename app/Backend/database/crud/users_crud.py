# 데이터 읽기
# Session를 sqlalchemy.orm사용하면 db매개변수의 유형을 선언하고 함수에서 더 나은 유형 검사 및 완성 기능을 사용할 수 있다.
# 가져오기 models(SQLAlchemy 모델) 및 schemas(Pydantic 모델 /스키마).

from sqlalchemy.orm import Session
from .. import models, schemas

# 비밀번호 해싱
import secrets
from passlib.context import CryptContext

# 비밀번호를 해싱화 하기 위한 곳
hasing = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해쉬 생성
def get_password_hash(password: str) -> str:
    return hasing.hash(password)
# 비밀번호 해쉬 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hasing.verify(plain_password, hashed_password)
# 토큰 생성
def generate_token() -> str:
    return secrets.token_urlsafe(32)

# 유저 한명 가져오기 
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 유저 이메일 가져오기
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
    
# 유저 비밀번호와 이메일 입력했는지 검증
def check_user_password_and_email(user: schemas.UserCreate):
    if not user.name or not user.email or not user.password:
        return True
    return False

# 데이터 생성 (Create)
def create_user(db: Session, user: schemas.UserCreate):
    passwd_hased = get_password_hash(user.password)
    #데이터로 SQLAlchemy 모델 인스턴스 를 만듭니다.
    db_user = models.User(name=user.name ,email=user.email, hashed_password=passwd_hased)
    # add해당 인스턴스 개체를 데이터베이스 세션에 추가합니다.
    db.add(db_user)
    # commit데이터베이스에 대한 변경 사항(저장되도록).
    db.commit()
    # refresh인스턴스(생성된 ID와 같은 데이터베이스의 새 데이터가 포함되도록)
    db.refresh(db_user)
    return db_user

# 유저 전체 가져오기 (Read)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 유저 정보 업데이트 (Udate)
def update_user(db: Session, user: schemas.userUpdate):
    update_email = user.email
    update_password = user.password

    db.query(models.User).filter(models.User.id == user.id).update({"email" : update_email, "hashed_password" : update_password})
    db.commit()
    return db.query(models.User).filter(models.User.id == user.id).first()

# 유저 정보 삭제하기 (Delete)
def delete_users(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()