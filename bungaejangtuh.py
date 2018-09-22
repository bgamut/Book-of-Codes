import urllib,urllib3, json, re,requests,time
from bs4 import BeautifulSoup
import urllib3
from sentiment import *
from urllib.parse import quote, parse_qs
import time
loginurl="http://m.bunjang.co.kr/login"
baseurl="http://m.bunjang.co.kr/search/products?"
someword="핫토이즈"
urladd=''
first_index=True





headers={
            'order':'popular',
            'page':'1',
            'q' : someword ,
            
        }
for key in headers:
    value=quote(headers[key])
    value=re.sub(r'/',r'%2F',value)
    if (first_index==True):
        urladd=urladd+key+'='+value
    else:
        urladd=urladd+'&'+key+'='+value
    first_index=False
#print(urladd)
url = baseurl + urladd
urllib3.disable_warnings()
http=urllib3.PoolManager()
response=http.request('GET',url)
r=requests.get(url, allow_redirects=True)
for resp in r.history:
    #print(r.url)
    pass
newurl=response.geturl()
new_response=requests.get(newurl)

from selenium import webdriver

pathtocdriver = "C:\SDKs\seleniumdriver\chromedriver.exe"
driver=webdriver.Chrome(executable_path=pathtocdriver)
driver.get(loginurl)
bungaeid=jd('localInfo.json')['bungaejangtuhid']
bungaepw=jd('localInfo.json')['bungaejangtuhpw']
oldtitle=driver.title
newtitle=driver.title
logged_in=False
profile_selected=False
#print(url)
notloggedin=True
while (notloggedin==True):
    newtitle = driver.title
    try:
    
        oldurl=driver.current_url
        newerurl=driver.current_url
        idelem = driver.find_element_by_name("phone")
        idelem.send_keys(bungaeid)
        pwelem = driver.find_element_by_name("password")
        pwelem.send_keys(bungaepw)
        idbuttonelem = driver.find_element_by_class_name("login-btn")
        idbuttonelem.click()
    except:
        pass
    notloggedin=False
while(newerurl==oldurl):
    newerurl=driver.current_url

driver.get(newurl)
html=driver.page_source
soup=BeautifulSoup(html, features='lxml')
prices=soup.findAll('div',attrs={'class':'product-price'},text=True)
for i in range(len(prices)):
    prices[i]=prices[i].text.strip
print(prices)
#wait(driver, 15).until_not(EC.title_is(title))

if __name__ == "__main__":
    """
    getToken(sys.argv)
    """
