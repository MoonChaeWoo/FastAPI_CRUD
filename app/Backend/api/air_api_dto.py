from pydantic import BaseModel
from typing import List, Optional

class airCondition(BaseModel):
    title : str
    pm10value24 : Optional[int] = None
    so2value>0.002
    pm10value>24
    o3grade : Optional[int] = None
    pm25flag>
    khaigrade : Optional[int] = None
    pm25value>13
    no2flag>
    stationname>광양 율촌
    no2value>0.006
    so2grade : Optional[int] = None
    coflag>
    khaivalue : Optional[int] = None
    covalue>0.2
    pm10flag>
    sidoname>전남
    pm25value24 : Optional[int] = None
    no2grade : Optional[int] = None
    o3flag>
    pm25grade : Optional[int] = None
    so2flag>
    cograde : Optional[int] = None
    datatime>2022-09-28 17:00
    pm10grade : Optional[int] = None
    o3value>0.044