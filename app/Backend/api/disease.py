import requests
from os import environ
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

# .env 환경파일 로드 
load_dotenv()

serviceKey = environ['SERVICEKEY']
# 공공데이터포털에서 제공해주는 키는 이미 URL Encoding이 되어있는 키인데 또다시 자체적으로 인코딩을 하여 2번이 되기에
# 디코딩을 해주어야 한다.
decode_key = requests.utils.unquote(serviceKey)

url = 'http://apis.data.go.kr/B550928/dissForecastInfoSvc/getDissForecastInfo'
params ={'serviceKey' : decode_key, 'numOfRows' : '22', 'pageNo' : '1', 'type' : 'JSON', 'dissCd' : '4', 'znCd' : '46' }


response = requests.get(url, params=params)
print(response.content.decode('utf8'))
# 'searchDate' : datetime.now().date() - timedelta(days=1) 하루 전 날짜
#content = response.text
#print(content)

def call_diease():

    json_list_disease = []

    try:
        response = requests.get(url, params=params).json()
        json_items = response['response']['body']['items']

        for item in json_items:
            # print(item)
            json_list_disease.append(item)

    except:
        json_list_disease = None
        #response = requests.get(url, params=params).text
        #response = json.dumps(response)
        #response = json.loads(response)
    #json_data = json.loads(response)
    return json_list_disease