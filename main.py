'''
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/bbc94440-2a57-4ffc-bea7-17e3c3d8e508' \
  -H 'accept: text/plain'
'''
import pprint

import requests

# url = "http://5.63.153.31:5051/v1/account"
# headres = {
#     'accept': '*/*',
# }
# json = {
#     "login": "janmes2",
#     "email": "jame2s@mail.ru",
#     "password": "12345678"
# }
#
# response = requests.post(
#     url=url,
#     headers=headres,
#     json=json
# )

url = "http://5.63.153.31:5051/v1/account/bbc94440-2a57-4ffc-bea7-17e3c3d8e508"
headres = {
    'accept': 'text/plain',
}


response = requests.put(
    url=url,
    headers=headres,
)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])