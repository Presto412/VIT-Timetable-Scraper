import FileUploadToDrive
from FileUploadToDrive import FileUpload
from PIL import Image
import mechanize,cookielib
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import json
from Captcha_Parser import CaptchaParse
import ssl
import re
import requests
import datetime


def calsem():
        now = datetime.datetime.now()
        if int(now.month)>6 and int(now.month)<13:
                sem="FS"
        else:
                sem="WS"
        return sem

br= mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)


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
captcha=CaptchaParse(imgcpy)


print "Recognized Captcha:"+str(captcha)
br.select_form('parent_login')

regno=raw_input("Registration Number:")
dob=raw_input("Date of Birth:")
mno=raw_input("Registered Parent Mobile Number:")
sem=calsem()
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
for i in row1:
        if i not in row2:
                row2.append(i)
#below code was for personal use, wanted to retrieve only slots and venues
"""
count=0
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
                       break;
"""
fout=open("Timetable of "+regno+".txt","w")
for i in venueslot:
        fout.write(i+'\n')
fout.close()
FileUpload(regno)
