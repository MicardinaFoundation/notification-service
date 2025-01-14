# -*- coding: utf-8 -*-
import sys
from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.header    import Header
from email.message    import EmailMessage
from twilio.rest import Client
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
app = Celery('tasks', broker='redis://localhost:6379/1')


@app.task
def send_email(subject, message, to_email):
    try:
        # Настройки SMTP
        sender_email = "sdgsp@inbox.ru"
        password = "eL11bQtsw7FmLkeNwa9k"

        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = sender_email
        msg['To'] = to_email

        # m = 'Subject: {}\n\n{}'.format(subject, message)

        # msg = EmailMessage()
        # msg.set_content(message)
        # msg['Subject'] = subject
        # msg['From'] = sender_email
        # msg['To'] = to_email
        


        # html = f"""
        # <html>
        #     <body>
        #         <h1>{subject}</h1>
        #         <p>{message}</p>
        #     </body>
        # </html>
        # """

        # msg.add_alternative(html, subtype = "html")
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        #server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
        
    except Exception as e:
        print(f'Eror: {e}')
    finally:
        print(msg)
        server.quit()
        
    
        



@app.task
def send_sms(message, recipient_phone):
    # Настройки Twilio
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    twilio_number = 'your_twilio_number'

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=recipient_phone
    )
