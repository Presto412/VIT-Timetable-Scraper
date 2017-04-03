import SendEmail
from SendEmail import SendEmail
from PIL import Image
import mechanize,cookielib
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import json
from CaptchaParser import CaptchaParser
import ssl
import re
import requests

br= mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

#SSL handler,made me go nuts at first
try:
        _create_unverified_https_context=ssl._create_unverified_context
except AttributeError:
        pass
else:
        ssl._create_default_https_context=_create_unverified_https_context
print "Fetching Captcha"        

r=br.open('https://vtop.vit.ac.in/parent/parent_login.asp')
html=r.read()
soup=BeautifulSoup(html)
im = soup.find('img', id='imgCaptcha')
image_response = br.open_novisit(im['src'])
img=Image.open(StringIO(image_response.read()))
imgcpy=img.copy()
parser=CaptchaParser()
captcha=parser.getCaptcha(img)


print "Recognized Captcha:"+str(captcha)
br.select_form('parent_login')

regno=raw_input("Registration Number:")
dob=raw_input("Date of Birth:")
mno=raw_input("Mobile Number:")
sem=raw_input("Semester(FS/WS):");
br.form['wdregno']=regno
br.form['vrfcd']=str(captcha)
br.form['wdpswd'] =dob 
br.form['wdmobno']=mno

print "Logging in User:"

response=br.submit()
if(response.geturl()=="https://vtop.vit.ac.in/parent/home.asp"):
        print "Successfully Logged In"
else:
        print "Recheck Credentials"
mainpage=br.open(response.geturl()).read()
mainsoup=BeautifulSoup(mainpage)
ttasp=br.open('https://vtop.vit.ac.in/parent/timetable.asp?sem='+sem)
tthtml=ttasp.read()
ttsoup=BeautifulSoup(tthtml)
row1=[]
row2=[]
table=ttsoup.find('table',attrs={'cellpadding':'2','border':'1','cellspacing':'0','width':'95%','style':'border-collapse: collapse'})
for mainrow in table.findAll("tr"):
        cells=mainrow.findAll('td',attrs={'bgcolor':'#CCFF33'})
        for i in cells:
                row1.append(i.find(text=True).encode("utf-8"))
#removes duplicates 
for i in row1:
        if i not in row2:
                row2.append(i)
count=0
#below code was for personal use, I needed only the slots and the venues
#the list row2 has the timetable in the format of [coursecode-coursetype-venue-slot], use it however
"""
venueslot=[]
venue=[]
slot=[]
for i in row2:
        for j in range(0,len(i)-1):
                if i[j]=='-':
                       count+=1
                if count==2:
                       newstr=i[j+2:len(i)]
                       venueslot.append(newstr)
                       count=0
                       break
"""
#writes the details to a textfile
fout=open("Timetable of "+regno+".txt","w")
for i in venueslot:
        fout.write(i+'\n')
fout.close()
#sends a copy of the text file generated as email
SendEmail(regno)
