import win32com.client

outlook = win32com.client.Dispatch('outlook.application')

mail = outlook.CreateItem(0)

mail.To = 'david.weyenschops@collaboration-factory.de'
mail.Subject = 'GitHub Access Approval'
mail.HTMLBody = '<h3>Please follow this link. https://www.youtube.com/watch?v=dQw4w9WgXcQ</h3>'
mail.Body = "Please follow this link. https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#mail.Attachments.Add('c:\\sample.xlsx')
#mail.Attachments.Add('c:\\sample2.xlsx')
#mail.CC = 'somebody@company.com'
mail.Send()