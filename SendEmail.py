#to send an email via a python script with an attachment,you have to enable less secure apps at the below link
#<<https://myaccount.google.com/lesssecureapps?pli=1>>

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
def SendEmail(regno): 
    fromaddr = "FROM ADDRESS"
    toaddr = "TO ADDRESS"
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
 #type in the subject of the mail
 #   msg['Subject'] = "TIME TABLE OF "+regno
     
 #   body = "The timetable of "+regno+" have been sent as an attachment."
     
    msg.attach(MIMEText(body, 'plain'))
     
 #  name of the file ,set it however
 #  filename = "Timetable of "+regno+".txt"
    attachment=open(filename,'rb')
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #enter your password here
    server.login(fromaddr, "YOUR PASSWORD HERE")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    
