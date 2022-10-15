import os
import smtplib, ssl
from datetime import datetime
#from pathlib import Path
from email.message import EmailMessage
from typing import Iterable


from scripts.setup import secrets, text_temp


src_email = secrets['gmail']['email_handler']['user']

def send_basic_mail(subject: str, recipient: str, body: str)-> None:
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = src_email
    msg['To'] = recipient
    msg.set_content(body)

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(src_email, secrets['gmail']['email_handler']['passWd'])
            server.sendmail(
                src_email,
                recipient.split(", "),
                msg.as_string()
            )

        with open("log.txt", "a") as log:
            log.write(f"pass\t{subject}\t{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\tsend_basic_mail\n")
    except BaseException as err:
        with open("log.txt", "a") as log:
            log.write(f"fail\t{subject}\t{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\t{err.__repr__()}\n")

def send_template_mail(template: str, recipient: str, params: Iterable)-> None:
    subject = text_temp[template]['subject']
    body = text_temp[template]['body'] % tuple(params)
    send_basic_mail(subject, recipient, body)


