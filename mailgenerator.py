import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

from random import randint

def Sending_report(mails):
    print('mail is sending.....wait.')
    now=datetime.now()
    t=now.strftime("%d/%m/%Y, %H:%M:%S")
    time=str(t)
    fromaddr = "example@gmail.com"  #email
    otp=randint(100000, 999999)
    print('OTP sent....',otp)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    for i in mails:
        msg['To'] = i
    msg['Subject'] = "OTP for the Depression Detection Application !"
    body = 'We are from depression detection application. \n This application helps you to analyse the social media text whether it is depressive or normal \nand to monitor the tweets on social media accounts of your subscribed users in this application \nand we will notify you whenever your subscribed account posts a depressive content on socila media. \n\nPlease enter this otp to complete your email verification:   '+str(otp)
    msg.attach(MIMEText(body, 'plain'))
    filename = "logo.png"
    attachment = open("logo.png", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p) #to attach a pdf
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr,"********") #Password
    text = msg.as_string()
    cnt=0
    for i in mails:
        s.sendmail(fromaddr,i, text)
        print('welcome mail sent successfully to '+i)
        cnt+=1
    print('Total Number of mails sent',cnt)
    # s.quit()
    return otp
