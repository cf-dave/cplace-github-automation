import requests

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
    #('filter', '$status$ = \'01 - Not started\''),
    ('selectedAttributes', 'subject, description, status'),
    ('limit', '50'),
)


r2 = requests.get('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/Incident/data/11063640', headers=headers)#, params=params)
print(r2)