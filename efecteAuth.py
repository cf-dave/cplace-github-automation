from asyncio import subprocess
import requests
import json
from subprocess import check_output
import win32com.client

#outlook = win32com.client.Dispatch('outlook.application')


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


r2 = requests.get('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data/12204512', headers=headers)#, params=params) #||||11133725
#print(r2.text)

#result = r2.text.replace("\\\"", "\"")

ticket = json.loads(r2.text)
serviceOffering = ticket['data']['ServiceOffering']['values'][0]['value']
#requestBundleName = ticket['data']['RequestBundleName']['values'][0]['value']
serviceItem = ticket['data']['ServiceItem']['values'][0]['name']                    ## Hier steht die Anfrage Art drin
additionalInformation = (ticket['data']['AdditionalInformation']['values'][0]['value']).split("\n")
#print(additionalInformation)

user = "cf-dave"
repo, level, justification = additionalInformation[0].split(':')[1], additionalInformation[1].split(':')[1],additionalInformation[2].split(':')[1]#,additionalInformation[3].split(':')[1]


#Debug prints
print(serviceOffering)
#print(requestBundleName)
print(serviceItem)
print(user)
print(repo)
print(level)
print(justification)


service = -1        ## Entscheidung welche Aktion ausgeführt wird

if serviceItem == "IT Repository | New":
    service = 1
elif serviceItem == "IT Repository | Access Request":
    service = 2
else:
    service = 0

if service==1:
    with open("todo.txt", 'w') as fd:
        print(repo)
        if(repo.startswith('cplace')):
            fd.write("repoName:"+ repo)
            p = check_output(['node', 'testJSOutput.js'])
            print (p)
        else:
            #reject for naming scheme
            print("Illegal name")
elif service == 2:
    with open("todo.txt", 'w') as fd:
        #print(repo)
        fd.write("user:"+ user+"\n")
        if(repo.startswith('cplace')):
            fd.write("repoName:"+ repo+"\n")
        fd.write("level:"+level+"\n")
        fd.write("justification:"+justification+"\n")  
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