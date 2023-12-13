import smtplib
from email.message import EmailMessage
import json

def send_mail(reciving_gmail_id,subject, message):
    data = json.load(open('config.json','r'))['params']
        
    # data for sending
    sender = data['gmail']
    password = data['password']
    
    reciver = reciving_gmail_id
    
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = reciver
    msg.set_content(message, subtype='html')


    # sending the otp to the gmail
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(msg)
    # exit the server
        smtp.quit()
    return  'done'
