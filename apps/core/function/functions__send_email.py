import base64
import smtplib


def send_mail(email, subject, text):
    sender_email = 'yulmarika@yandex.ru'
    password = 'Cr3-XK5-db8-CRf'
    server = smtplib.SMTP_SSL('smtp.yandex.com')
    server.set_debuglevel(1)
    server.ehlo(email)
    server.login(sender_email, password)
    server.auth_plain()
    message = "From: {}\nTo: {}\nSubject: {}\n\n{}.".format(sender_email, email, subject, text)
    # message = u' '.join((agent_contact, agent_telno)).encode('utf-8').strip()
 
    server.sendmail(sender_email, email, message.encode('utf-8'))
    server.quit()