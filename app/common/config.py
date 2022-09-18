from dataclasses import dataclass, asdict
from os import path, environ
# 환경별 변수를 넣는 파일
# 서버 운영 시 상황에 따라 다른 방법으로 설정 파일을 넣는 파일

base_dir = path.dirname(p)

# LocalConfig와 ServerConfig의 베이스 클래스
@dataclass
class Config:
    BASE_DIR = base_dir

    DB_POOL_RECYCLE : int = 900
    DB_ECHO : BOOL = True
