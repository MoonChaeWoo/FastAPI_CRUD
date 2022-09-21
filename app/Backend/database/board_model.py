from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .conn import Base

class User(Base):
    # __tablename__속성은 SQLAlchemy에게 이러한 각 모델에 대해 데이터베이스에서 사용할 테이블 이름을 알려줍니다 .
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # relationship은 관계를 위해 SQLAlchemy ORM에서 제공하는 것을 사용 한다.
    # 변수명 = relationship("관계할 클래스명", back_populates="관계하는 클래스 안에 있는 relationship의 변수 이름")
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # relationship은 관계를 위해 SQLAlchemy ORM에서 제공하는 것을 사용 한다.
    owner = relationship("User", back_populates="items")