import base64
import smtplib
from apps.filecodes.models import YandexMailAPI


def send_mail(email, subject, text):
    api = YandexMailAPI.objects.first()
    if api and api.email and api.password and api.smtp:
        sender_email = api.email
        password = api.password
        server = smtplib.SMTP_SSL(api.smtp)
    else:
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