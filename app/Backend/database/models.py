# SQLAlchemy 스타일과 Pydantic 스타일
# SQLAlchemy 모델 은 를 사용하여 속성을 정의 하고 다음 =과 같이 유형을 매개변수로 전달
# ex) name = Column(String)

# Pydantic 모델: 은 새로운 유형 주석 구문/유형 힌트 를 사용하여 유형을 선언합니다 .
# ex) name: str
# =이 점을 염두에 두어 사용 시 혼동되지 않는다. 

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from pydantic import BaseModel, Field

from .conn import Base

class User(Base):
    # __tablename__속성은 SQLAlchemy에게 이러한 각 모델에 대해 데이터베이스에서 사용할 테이블 이름을 알려준다.
    # 생성한 Base를 기반으로 모델을 만들어낸다.
    # _tablename_ 을 필수적으로 선언해야한다.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(60))

    is_active = Column(Boolean, default=True)

    # relationship은 관계를 위해 SQLAlchemy ORM에서 제공하는 것을 사용 한다.
    # 변수명 = relationship("관계할 클래스명", back_populates="관계하는 클래스 안에 있는 relationship의 변수 이름")
    # back_populate : relation에서 연결된 부분에서 접근할시의 이름
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    description = Column(String(50), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    # relationship은 관계를 위해 SQLAlchemy ORM에서 제공하는 것을 사용 한다.
    # back_populate : relation에서 연결된 부분에서 접근할시의 이름
    owner = relationship("User", back_populates="items")

# 토큰 생성
# def generate_token() -> str:
#     return secrets.token_urlsafe(32)
