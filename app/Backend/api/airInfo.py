import requests
import base64

serviceKey = '3%2FXE8PU0Cz7plOdNzmb73e7Nwmp0%2B8geWSkHauYkfi7uOSvinwVnwS%2BT2R9u4HSnXx8B51Az%2BFALxKJ81RKQPQ%3D%3D'

# 공공데이터포털에서 제공해주는 키는 이미 URL Encoding이 되어있는 키인데 또다시 자체적으로 인코딩을 하여 2번이 되기에
# 디코딩을 해주어야 한다.
decode_key = requests.utils.unquote(serviceKey)

url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
params ={'serviceKey' : decode_key, 'returnType' : 'xml', 'numOfRows' : '100', 'pageNo' : '1', 'sidoName' : '서울', 'ver' : '1.0' }

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
print(response.content)

# 응답은 3가지 형태로 올 수 있다.
# 1. 첫 번째는 content 속성을 통해 바이너리 원문을 얻을 수 있습니다.
# 2. 두 번째는 text 속성을 통해 UTF-8로 인코딩된 문자열을 얻을 수 있습니다.
# 3. 마지막으로, 응답 데이터가 JSON 포멧이라면 json() 함수를 통해 사전(dictionary) 객체를 얻을 수 있습니다.
# 응답에 대한 메타 데이터를 담고 있는 응답 헤더는 headers 속성을 통해 사전의 형태로 얻을 수 있습니다.
# print(response.headers)