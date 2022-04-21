from asyncio import subprocess
import requests
import json
from subprocess import check_output
import win32com.client




headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
  'login': 'restp-api-test',
  'password': 'Cplace123!'
}

response = requests.post('https://cplace.efectecloud-test.com/rest-api/itsm/v1/users/login', headers=headers, data=data)
print(response)
token = response.headers['Authorization'].split(' ')[1]
print(token)

headers = {
    'accept': 'application/json',
    'Authorization' : ('Bearer '+ token),
}

params = (
    #('filter', '$Self-Service Item$ = \'IT Repository | New\''),
    ('selectedAttributes', 'Subject, request_service, status, ServiceItem'),
    ('limit', '50'),
    ('filterId', '1000000000'),
)

employeesList = []

with open("actions-data.json", 'r') as fd:
    employeesList = json.loads(fd.read())

descriptions = []

for employee in employeesList:
    firstName = employee["attributes"]["first_name"]["value"]
    lastName = employee["attributes"]["last_name"]["value"]
    email = employee["attributes"]["email"]["value"]
    position = employee["attributes"]["position"]["value"]
    employment = employee["attributes"]["employment_type"]["value"]
    hireDate = employee["attributes"]["hire_date"]["value"]
    office = employee["attributes"]["office"]["value"]["attributes"]["name"]
    departmnet = employee["attributes"]["department"]["value"]["attributes"]["name"]
    secondMail = employee["attributes"]["dynamic_676432"]["value"] 
    language = employee["attributes"]["dynamic_2690447"]["value"] 
    contract = employee["attributes"]["dynamic_546104"]["value"] 
    descriptions.append(firstName + "\n" + lastName + "\n" + email + "\n" + position + "\n" + employment + "\n" + str(hireDate) + "\n" + office + "\n" + departmnet + "\n" + secondMail + "\n" + language + "\n" + contract )
    #print(descriptions.pop())

for description in descriptions:
    body = {
    "folderCode": "ServiceRequest",
    "data": {
        "Subject": {
            "values": [
                {
                    "value": "Onboarding for" + firstName + " " + lastName + " on " + hireDate
                }
            ]
        },
        "RequestedFor": {
            "values": [
                {
                    "value": "David Weyenschops"
                }
            ]
        },
        "ServiceItem": {
            "values": [
                {
                    "value": "Generic Service Request"
                }
            ]
        },
        "description": {
            "values": [
                {
                "value": descriptions
                }
            ]
        }
    }
    }
    result = requests.post('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data?dataCards=true', json = body, headers=headers)
    print(result)
    print(result.text)