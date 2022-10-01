import requests
from os import environ
from dotenv import load_dotenv
import json

# .env 환경파일 로드 
load_dotenv()

serviceKey = environ['SERVICEKEY']
# 공공데이터포털에서 제공해주는 키는 이미 URL Encoding이 되어있는 키인데 또다시 자체적으로 인코딩을 하여 2번이 되기에
# 디코딩을 해주어야 한다.
decode_key = requests.utils.unquote(serviceKey)

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
params ={'serviceKey' : decode_key, 'returnType' : 'JSON', 'numOfRows' : '100', 'pageNo' : '1', 'sidoName' : '전남', "ver" : '1.1'}

response = requests.get(url, params=params)

content = response.text

json_data = json.loads('content')

json_items = json_data['response']['body']['items']

json_list = []

for item in json_items:
    json_list.append(item)