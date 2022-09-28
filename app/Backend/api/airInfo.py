import requests
import base64
from os import environ
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from xml.etree.ElementTree import parse



# .env 환경파일 로드 
load_dotenv()

serviceKey = environ['SERVICEKEY']
# 공공데이터포털에서 제공해주는 키는 이미 URL Encoding이 되어있는 키인데 또다시 자체적으로 인코딩을 하여 2번이 되기에
# 디코딩을 해주어야 한다.
decode_key = requests.utils.unquote(serviceKey)

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
params ={'serviceKey' : decode_key, 'returnType' : 'XML', 'numOfRows' : '100', 'pageNo' : '1', 'searchDate' : '2022-09-24', 'InformCode' : 'PM10' }

# requests 라이브러리는 매우 직관적인 API를 제공한다.
# 어떤 방식(method)의 HTTP 요청을 하느냐에 따라서 해당하는 이름의 함수를 사용하면 된다.
# GET 방식: requests.get()
# POST 방식: requests.post()
# PUT 방식: requests.put()
# DELETE 방식: requests.delete()

# 상태 코드는 응답 객체의 status_code 속성을 통해 간단하게 얻을 수 있다.
# print(response.status_code)

response = requests.get(url, params=params)
# print(response.status_code) # result 200
# print(response.content)
# print(response.content.decode('utf8'))

# 먼저 디코딩을 해줌
items = response.content.decode('utf8')

tree = parse(items)
root = tree.getroot()
# 위와 같이 2줄로 하는 방법이 있으며
# root = ET.fromstring(items)

print(root)




#dict_type = xmltodict.parse(items)

# print(dict_type)

#json_type = json.dumps(dict_type)
#dict2_type = json.loads(json_type)

#print(dict2_type)

#print('------------------------------')

#print(dict2_type['dataTime'])



# 응답은 3가지 형태로 올 수 있다.
# 1. 첫 번째는 content 속성을 통해 바이너리 원문을 얻을 수 있습니다.
#    - response.content.decode('utf8') 이렇게 디코딩을 하면 된다.
# 2. 두 번째는 text 속성을 통해 UTF-8로 인코딩된 문자열을 얻을 수 있습니다.
# 3. 마지막으로, 응답 데이터가 JSON 포멧이라면 json() 함수를 통해 사전(dictionary) 객체를 얻을 수 있습니다.
# 응답에 대한 메타 데이터를 담고 있는 응답 헤더는 headers 속성을 통해 사전의 형태로 얻을 수 있습니다.
# print(response.headers)
