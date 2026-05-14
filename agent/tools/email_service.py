import smtplib
from email.message import EmailMessage
from agent.config import settings


def email_sender(receiver_emailAddress:str,body:str,subject:str):
    try:
        msg =EmailMessage()
        msg['Subject'] = subject
        msg['From'] = settings.SENDER_EMAIL_ADDRESS
        msg['To'] = receiver_emailAddress
        msg.set_content(body)   
        with smtplib.SMTP('smtp.gmail.com',587,timeout=10) as s:
            s.starttls()
            s.login(settings.SENDER_EMAIL_ADDRESS,settings.EMAIL_APP_PASSWORD)
            s.send_message(msg)
            
        return f"Email successfully sent to {receiver_emailAddress}"
    except Exception as e:
        return f"error: Email isn't send to {receiver_emailAddress} due to {e}"
    
# email_sender('youremail@gmail.com','email checking body','subject checking')