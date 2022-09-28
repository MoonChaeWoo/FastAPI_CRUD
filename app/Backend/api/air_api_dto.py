from datetime import date
from pydantic import BaseModel
from typing import Optional
from dataclasses import dataclass

@dataclass
class airCondition(BaseModel):
    pm10value24 : Optional[int] = None      # 미세먼지 pm10 24시간 예측 이동농도
    so2value : Optional[float] = None       # 아환산가스 지수
    pm10value : Optional[int] = None        # 미세먼지 pm10 농도
    o3grade : Optional[int] = None          # 오존 지수
    pm25flag : Optional[str] = None         # 미세먼지 플래그
    khaigrade : Optional[int] = None        # 통합대기환경 지수
    pm25value : Optional[int] = None        # 미세먼지 24시간 예측이동농도
    no2flag : Optional[str] = None          # 이산화질소 플래그
    stationname : Optional[str] = None      # 측정소 명
    no2value : Optional[float] = None       # 이산화질수 지수
    so2grade : Optional[int] = None         # 아황산가스 지수
    coflag : Optional[str] = None           # 일산화탄소 플래그
    khaivalue : Optional[int] = None        # 통합대기환경수치
    covalue : Optional[float] = None        # 일산화탄소 농도
    pm10flag : Optional[str] = None         # 미세먼지 플래그
    sidoname : Optional[str] = None         # 시도명
    pm25value24 : Optional[int] = None      # 미세먼지 pm25 24시간 예측 이동농도
    no2grade : Optional[int] = None         # 이산화질소 지수
    o3flag : Optional[str] = None           # 오존 플래그
    pm25grade : Optional[int] = None        # 미세먼지 pm25 플래그
    so2flag : Optional[str] = None          # 아환산가스 플래그
    cograde : Optional[int] = None          # 일산화탄소지수
    datatime : Optional[date] = None        # 측정 일시
    pm10grade : Optional[int] = None        # 미세먼지 24시간 등급자료
    o3value : Optional[float] = None        # 오존 농도