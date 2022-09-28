import requests
from bs4 import BeautifulSoup
from os import environ
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
import re



# .env 환경파일 로드 
load_dotenv()

serviceKey = environ['SERVICEKEY']
# 공공데이터포털에서 제공해주는 키는 이미 URL Encoding이 되어있는 키인데 또다시 자체적으로 인코딩을 하여 2번이 되기에
# 디코딩을 해주어야 한다.
decode_key = requests.utils.unquote(serviceKey)

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
params ={'serviceKey' : decode_key, 'returnType' : 'XML', 'numOfRows' : '100', 'pageNo' : '1', 'sidoName' : '전남', "ver" : '1.1'}

response = requests.get(url, params=params)

#print(response.url)

content = response.text

#print(content)
print('**********************')
#print(content)
soup = BeautifulSoup(content, 'html.parser')
data = soup.find_all('item')

list = []

for item in data:
    list.append(item)

for i in list:
    print("--------")
    print(i)
    print("--------")


print('**********************')

# print(content)

