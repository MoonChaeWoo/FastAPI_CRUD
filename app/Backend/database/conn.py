# pip3 install sqlalchemy
# ORM을 통하여 DB 쿼리문을 작성하기 위해 설치

# pip3 install python-dotenv
# DB관련 정보를 입력할 때, 환경변수를 통하여 내용을 입력하기 위해 dotenv 설치
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
from dotenv import load_dotenv
# import pandas as pd

# .env 환경파일 로드 
load_dotenv()

SQLALCHEMY_DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
    environ['DB_TYPE'],
    environ['DB_USER'],
    environ['POSTGRES_PASSWORD'],
    environ['DB_HOST'],
    environ['DB_PORT'],
    environ['POSTGRES_DB'],
)

# SQLALCHEMY_DATABASE_URL2 = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
# SQLALCHEMY_DATABASE_URL 데이터 원본 이름 : 데이터베이스에 대한 연결을 설정하도록 함

engin = create_engine(SQLALCHEMY_DATABASE_URL, echo = True, encoding='utf-8', pool_pre_ping=True)
# 위 명령이 DB에 바로 연결시키는건 아니고, 이제 메모리에 인식 시키는 상황이다.
# echo를 true로 설정하면 command창에 실행된 sql문이 뜨게 됨
# engin변수는 sqlalchemy engine을 만드는것이며 나중에 main.py 폴더에서 사용할 예정
# pool_recycle 시간 초과 연결 및 데이터베이스 다시 시작을 처리하기 위한 여러 기술
# create_engine =("check_same_thread": False)는 SQLite에만 필요하며 다른 데이터베이스에는 필요하지 않는다.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)
# 각각의 SessionLocal 클래스 객체는 데이타베이스의 세션이 된다.
# 클래스 자체는 아직 데이터베이스 세션이 아니다. 그러나 SessionLocal클래스의 인스턴스를 생성하면 이 인스턴스가 실제 데이터베이스 세션이 됩니다.
# 변수명은 SessionLocal로 한다. 추후 사용할 Session과 이름 충돌을 막기 위해서이다.
# SessionLocal클래스 를 생성하려면 sessionmaker라는 함수를 사용하여야 한다.

Base = declarative_base()
# declarative_base()이제 클래스를 반환하는 함수를 사용할 것이다.
# 이 클래스에서 상속하여 각 데이터베이스 모델 또는 클래스(ORM 모델)를 생성한다.





# # 테이블 이름 변수
# table_names = engin.table_names()

# # 테이블 이름 변수 출력
# print(table_names)

# # DB와의 연결
# con = engin.connect()

# # Query의 실행
# rs = con.execute("SELECT * FROM board")

# # df에 Query의 결과를 저장
# df = pd.DataFrame(rs.fetchall())

# # DB 끊기
# con.close()

# # DataFrame head 출력
# print(df.head())