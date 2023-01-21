# FastAPI에는 Schema라는 개념이 존재한다
# 스프링이나 nestJS로 개발을 해봤던 사람이라면 DTO라는 이름이 더 익숙할 것
# DTO란 Data Transfer Object의 약자로서 어떤 메소드나 클래스간 객체정보를 주고 받을 때 특정 모양으로 주고 받겠다는 일종의 약속
# FastAPI의 스키마는 pydantic model에 종속돼있다. 

from typing import List
from pydantic import BaseModel, Field
from fastapi import Form, File, UploadFile

# item 스키마
class ItemBase(BaseModel):
    title : str
    description: str | None = None

class ItemCreate(ItemBase):
    uploadFile : UploadFile | None = None

    @classmethod
    def as_form(cls, title : str = Form(...), description : str = Form(...), uploadFile : UploadFile | None = None):
        return cls(title = title, description = description, uploadFile = uploadFile)

class ItemUpdate(ItemCreate):
    id : int

class ItemDelete(BaseModel):
    id : int

    @classmethod
    def as_form(cls, id : int = Form(...)):
        return cls(id = id)

class Item(ItemBase):
    id : int
    owner_id : int

    class Config:
        orm_mode = True
        # pydantic에서 제공하는 orm_mode를 이용하여 반환 모델을 만들 경우, ORM JSONEncoder에 의해 자동으로 json으로
        # 변환해주기 때문에 별도로 JSONResponse 등의 객체를 이용할 필요가 없다.
        # 이렇게 하면 다음 과 같이 에서 id값 을 가져오려고만 하는 대신 dict다음과 같이 됩니다.
        # 즉 config.py에서 사용하던 @dataclass를 사용한 효과를 볼 수 있다는 의미이다.

        # ex) id = data["id"] 또는 id = data.id
        # 이를 통해 Pydantic 모델 은 ORM과 호환되며 경로 작업response_model 의 인수에서 선언할 수 있다 .
        # 데이터베이스 모델을 반환할 수 있으며 데이터베이스 모델에서 데이터를 읽는다.

# user 스키마
class UserBase(BaseModel):
    name : str
    email : str

class UserCreate(UserBase):
    password : str

    # 아래와 같이 classmethod를 생성해주어야 jinja2에서 ajax 데이터를 보내면 받을 수 있다.
    # @staticmethod도 있음
    @classmethod
    def as_form(cls, name : str = Form(...), email : str = Form(...), password : str = Form(...)):
        return cls(name = name, email = email, password = password)

class userUpdate(UserCreate):
    id : int

class UserLogin(UserCreate):
    class Config:
        orm_mode = True

class User(UserBase):
    id : int
    is_active : bool
    items : List[Item] = []

    class Config:
        orm_mode = True

# jwt를 위한 class
class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None