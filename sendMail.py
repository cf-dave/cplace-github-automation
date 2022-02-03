from operator import le
import win32com.client

with open("todo.txt", 'r') as fd:
    values = fd.read().split("\n")

print(values)
user, repo, level, justification = values[0].split(':')[1], values[1].split(':')[1],values[2].split(':')[1],values[3].split(':')[1]
print(user + repo + level + justification)


outlook = win32com.client.Dispatch('outlook.application')

mail = outlook.CreateItem(0)

mail.To = 'david.weyenschops@collaboration-factory.de'
mail.Subject = 'GitHub Access Approval'
mail.HTMLBody = '<h3>The user ' + user + ' wants to have ' + level + 'permission to the repo ' + repo +'. The justification for this action is ' + justification+ '.Please follow this link to approve or deny the request. https://www.youtube.com/watch?v=dQw4w9WgXcQ</h3>'
mail.Body = "The user ' + user+ ' wants to have ' + level + 'permission to the repo ' + repo +'. The justification for this action is ' + justification+ '.Please follow this link to approve or deny the request. https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#mail.Attachments.Add('c:\\sample.xlsx')
#mail.Attachments.Add('c:\\sample2.xlsx')
#mail.CC = 'somebody@company.com'
mail.Send()
