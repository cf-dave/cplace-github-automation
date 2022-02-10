from asyncio import subprocess
import requests
import json
from subprocess import check_output
import win32com.client
import smtplib, ssl
from email.mime.text import MIMEText


host = 'smtp.office365.com'
port = 587

url = 'https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data/'
dc_url = 'https://cplace.efectecloud-test.com/itsm/EfecteFrameset.do#/workspace/datacard/view/'


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
    ('selectedAttributes', 'subject, request_service, status, ServiceItem, direktLink, AdditionalInformation'),
    ('limit', '50'),
    ('filterId', '1000000000'),
)


def sendEmail(link):
    sender = 'david.weyenschops@collaboration-factory.de'
    receivers = ['david.weyenschops@collaboration-factory.de']

    text_subtype = 'plain'
    content = 'The user ' + user+ ' wants to have ' + level.lower() + ' permission to the repo ' + repo +'. The justification for this action is \"' + justification+ '\". Please follow this link to approve or deny the request: ' + link

    subject = "Sent from python"
    
    try:
        smtpObj = smtplib.SMTP(host, port)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login('david.weyenschops@collaboration-factory.de', 'DelfinFlosse45')
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender
        smtpObj.sendmail(sender,receivers,msg.as_string())
        print("Success")
        smtpObj.quit()
    except:
        print("Error")


r2 = requests.get('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data/12204626', headers=headers)#, params=params) #||||11133725
r3 = requests.get('https://cplace.efectecloud-test.com/rest-api/itsm/v1/dc/ServiceRequest/data', headers=headers, params=params)
#print(r2.text)
r2T = json.loads(r2.text)
r3T = json.loads(r3.text)
dataCards = r3T['data']
#print(r2T)

notStarted = []
approved = []
for datacard in dataCards:     #Go through and filter the git hub ones out

    if len(datacard['data']['request_service']['values']) > 0:
        if datacard['data']['request_service']['values'][0]['name'] == 'GitHub Management':
            service = datacard['data']['ServiceItem']['values'][0]['name']
            status = datacard['data']['status']['values'][0]['value']
            id = datacard['dataCardId']
            if status == '01 - Not started':
                print(status)
                notStarted.append([id, service])
            elif status == '03 - Approved' :
                print(status)
                approved.append([id, service])
            else:
                continue
ghRequests = [notStarted, approved]

print(len(notStarted))

for ticket in notStarted:
    response = requests.get(url+str(ticket[0]), headers=headers, params=params)
    text = json.loads(response.text)
    print(text)
    serviceOffering = text['data']['ServiceOffering']['values'][0]['value']
    serviceItem = text['data']['ServiceItem']['values'][0]['name']     
    #link = text['data']['direktLink']['values'][0]['value']
    additionalInformation = (text['data']['AdditionalInformation']['values'][0]['value']).split(" ")
    #print(additionalInformation)
    user = "cf-dave"
    repo, level, justification = additionalInformation[1].split(':')[1], additionalInformation[3].split(':')[1],additionalInformation[4].split(':')[1]#,additionalInformation[3].split(':')[1]
    if level == "Read":
        level = "pull"
    elif level == "Write":
        level = "push"
    link = dc_url + ticket[0]

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
                p = check_output(['node', 'createRepo.js'])
                if p == "Script ran through":
                    print("Script ran through")
            else:
                #reject for naming scheme
                print("Illegal name")
    elif service == 2:
        with open("todo.txt", 'w') as fd:
                #print(repo)
                fd.write("user:"+ user+"\n")
                #if(repo.startswith('cplace')):
                fd.write("repoName:"+ repo+"\n")
                fd.write("level:"+level+"\n")
                fd.write("justification:"+justification+"\n")  
    sendEmail(link)



"""
status = ticket['data']['status']['values'][0]['value']
serviceOffering = ticket['data']['ServiceOffering']['values'][0]['value']
serviceItem = ticket['data']['ServiceItem']['values'][0]['name']                    ## Hier steht die Anfrage Art drin
additionalInformation = (ticket['data']['AdditionalInformation']['values'][0]['value']).split("\n")
print(status)

user = "cf-dave"
repo, level, justification = additionalInformation[0].split(':')[1], additionalInformation[1].split(':')[1],additionalInformation[2].split(':')[1]#,additionalInformation[3].split(':')[1]

if level == "Read":
    level = "pull"
elif level == "Write":
    level = "push"

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
            p = check_output(['node', 'createRepo.js'])
            if p == "Script ran through":
                print("Script ran through")
        else:
            #reject for naming scheme
            print("Illegal name")
elif service == 2:
    with open("todo.txt", 'w') as fd:
            #print(repo)
            fd.write("user:"+ user+"\n")
            #if(repo.startswith('cplace')):
            fd.write("repoName:"+ repo+"\n")
            fd.write("level:"+level+"\n")
            fd.write("justification:"+justification+"\n")  
    if(status == "01 - Not started"):

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
        
if(status == "03 - Approved"):
    #start js script
    p = check_output(['node', 'AddUserToRepo.js'])
    if p == "Script ran through":
        print("addToRepo succesful")
else:
    ("Illegal status")
