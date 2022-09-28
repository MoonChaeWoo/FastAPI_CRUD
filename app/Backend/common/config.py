from dataclasses import dataclass, asdict
from os import path, environ
# 환경별 변수를 넣는 파일
# 서버 운영 시 상황에 따라 다른 방법으로 설정 파일을 넣는 파일

# LocalConfig와 ServerConfig의 베이스 클래스
# dataclass 어노테이션은 해당 클래스를 Dict 형태로 추출해서 사용을 위함.
# print(asdict(LocalConfig()))하면 dict형태로 출력 

@dataclass
class Config:

    # __file__ : 현재 실행되고 있는 코드의 위치
    # path.dirname : 현재 파일을 갖고 있는 디렉터리의 명까지만 가져옴
    # print(base_dir) 최상위 디렉터리
    BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    FRONTEND = path.join(BASE_DIR, 'Frontend')
    STATIC = path.join(FRONTEND, 'static')
    TEMPLATES = path.join(FRONTEND, 'templates')
    BOARD = path.join(TEMPLATES, 'board')
    DASHBOARD = path.join(TEMPLATES, 'dashboard')
    
# Timeout 최대값
# template.yaml 파일에서 Timeout 값을 3600 으로 수정한 후, 배포 명령어 실행함.

# [오류 원인]
# Timeout의 최대값은 900

#[해결 방법]
#Timeout 값을 3600 → 900 으로 수정

    # DB_POOL_RECYCLE : int = 900
    # DB_ECHO : bool = True

# 로컬서버 (개발 서버)
@dataclass
class LocalConfig(Config):
    SERVER_RELOAD: bool = True

# 운영서버 (실제 서버)
@dataclass
class ServerConfig(Config):
    SERVER_RELOAD: bool = False

def conf():
    """
    환경 불러오기
    :return:

    API_ENV를 확인하여 환경을 정의한다. 만약 환경변수가 없으면 local 설정을 적용한다.
    """
    config = dict(server=ServerConfig(), local=LocalConfig())
    # os.environ
    return config.get(environ.get("API_ENV", "local"))