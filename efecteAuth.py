import requests
import json

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
  'login': 'restp-api-test',
  'password': 'Cplace123!'
}

response = requests.post('https://cplace.efectecloud-test.com/rest-api/itsm/v1/users/login', headers=headers, data=data)
token = response.headers['Authorization'].split(' ')[1]
print(token)

headers = {
    'accept': 'application/json',
    'Authorization' : ('Bearer '+ token),
}

params = (
    #('filter', '$Self-Service Item$ = \'IT Repository | New\''),
    ('selectedAttributes', 'subject, description, status'),
    ('limit', '50'),
    ('filterId', '1000000000'),
)


r2 = requests.get('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data/11133725', headers=headers)#, params=params)
print(r2.text)

with open("result1.json", 'w') as fd:
    json.dump(r2.text, fd)