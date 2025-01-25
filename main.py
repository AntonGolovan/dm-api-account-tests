"""
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "string",
  "email": "string",
  "password": "string"
}'
"""
import pprint

import requests as req

url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# payload = {
#     "login": "golovan3",
#     "email": "golovan3@mail.ru",
#     "password": "111222333"
# }
#
# responce = req.post(
#     url=url,
#     headers=headers,
#     json=payload
# )
#
# print(responce.status_code)
# # pprint.pprint(responce.json())


### ACTIVATE USERS

# user - golovan3
token = '/a160e1f3-2298-4914-a93c-ae3f0bbbf9f4'

"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/a160e1f3-2298-4914-a93c-ae3f0bbbf9f4' \
  -H 'accept: text/plain'
"""
headers = {
    'accept': 'text/plain',
}

responce = req.put(
    url=f'{url}{token}',
    headers=headers,
)

print(responce.status_code)
pprint.pprint(responce.json())
responce_json = responce.json()
print(responce_json['resource']['rating']['quantity'])
