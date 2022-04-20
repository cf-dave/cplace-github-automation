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
token = response.headers['Authorization'].split(' ')[1]
print(token)

headers = {
    'accept': 'application/json',
    'Authorization' : ('Bearer '+ token),
}

params = (
    #('filter', '$Self-Service Item$ = \'IT Repository | New\''),
    ('selectedAttributes', 'subject, request_service, status, ServiceItem'),
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
        "description": {
            "values": [
                {
                "value": "Onboarding for" + firstName + " " + lastName + " on " + hireDate
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
    body = json.dumps(body, indent=4)
    result = requests.post('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data', data = body)
    print(result)
exit()


r2 = requests.get('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data/12204626', headers=headers)#, params=params) #||||11133725
r3 = requests.get('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data', headers=headers, params=params)
#print(r2.text)
r2T = json.loads(r2.text)
r3T = json.loads(r3.text)
dataCards = r3T['data']

for datacard in dataCards:     #Go through and filter the git hub ones out
    notStarted = []
    approved = []
    if len(datacard['data']['request_service']['values']) > 0:
        if datacard['data']['request_service']['values'][0]['name'] == 'GitHub Management':
            service = datacard['data']['ServiceItem']['values'][0]['name']
            status = datacard['data']['status']['values'][0]['value']
            id = datacard['dataCardId']
            if status == '01 - Not started':
                notStarted.append([id, service])
            elif status == '03 - Approved' :
                approved.append([id, service])
            else:
                continue
ghRequests = [notStarted, approved]



ticket = json.loads(r2.text)
status = ticket['data']['status']['values'][0]['value']
serviceOffering = ticket['data']['ServiceOffering']['values'][0]['value']
#requestBundleName = ticket['data']['RequestBundleName']['values'][0]['value']
serviceItem = ticket['data']['ServiceItem']['values'][0]['name']                    ## Hier steht die Anfrage Art drin
additionalInformation = (ticket['data']['AdditionalInformation']['values'][0]['value']).split("\n")
print(status)

#user = "cf-dave"
#repo, level, justification = additionalInformation[0].split(':')[1], additionalInformation[1].split(':')[1],additionalInformation[2].split(':')[1]#,additionalInformation[3].split(':')[1]

lines = dict()
for line in additionalInformation:
    lines[line.split(':')[0]] = line.split(':')[1]


#if level == "Read":
#    level = "pull"
#elif level == "Write":
#    level = "push"

"""#Debug prints
print(serviceOffering)
#print(requestBundleName)
print(serviceItem)
print(user)
print(repo)
print(level)
print(justification)
"""

service = -1        ## Entscheidung welche Aktion ausgeführt wird

if serviceItem == "IT Repository | New":
    service = 1
elif serviceItem == "IT Repository | Access Request":
    service = 2
else:
    service = 0

with open("todo.json", 'w') as outfile:
        json.dump(lines, outfile)


if service==1:
    p = check_output(['node', 'createRepo.js'])
    if p == "Script ran through":
        print("Script ran through")
    else:
        #Error
        print("Error ocurred")
elif service == 2:
    if(status == "01 - Not started"):
        """
        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = 'david.weyenschops@collaboration-factory.de'
        mail.Subject = 'GitHub Access Approval'
        mail.HTMLBody = '<h3>The user ' + user + ' wants to have ' + level.lower() + ' permission to the repo ' + repo +'. The justification for this action is \"' + justification+ '\". Please follow this link to approve or deny the request. https://www.youtube.com/watch?v=dQw4w9WgXcQ</h3>'
        mail.Body = 'The user ' + user+ ' wants to have ' + level.lower() + ' permission to the repo ' + repo +'. The justification for this action is \"' + justification+ '\". Please follow this link to approve or deny the request. https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        #mail.Attachments.Add('c:\\sample.xlsx')
        #mail.Attachments.Add('c:\\sample2.xlsx')
        #mail.CC = 'somebody@company.com'
        mail.Send()
            #email out
        """
    elif(status == "03 - Approved"):
        #start js script
        p = check_output(['node', 'AddUserToRepo.js'])
        if p == "Script ran through":
            print("addToRepo succesful")
    else:
        ("Illegal status")
else:
    print("Illegal request")

"""
mail = outlook.CreateItem(0)

    mail.To = 'david.weyenschops@collaboration-factory.de'
    mail.Subject = 'GitHub Access Approval'
    mail.HTMLBody = '<h3>Please follow this link. https://www.youtube.com/watch?v=dQw4w9WgXcQ</h3>'
    mail.Body = "Please follow this link. https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    #mail.Attachments.Add('c:\\sample.xlsx')
    #mail.Attachments.Add('c:\\sample2.xlsx')
    #mail.CC = 'somebody@company.com'
    mail.Send()
"""