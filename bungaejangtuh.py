import urllib,urllib3, json, re,requests,time
from bs4 import BeautifulSoup
import urllib3
from sentiment import *
from urllib.parse import quote, parse_qs
import time
import re
import math
def getData(someword):
    loginurl="http://m.bunjang.co.kr/login"
    baseurl="http://m.bunjang.co.kr/search/products?"
    someword=someword
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
    #time.sleep(20)
    loaded=False
    while(loaded==False):
        try:    
            price=soup.find('div',attrs={'class':'product-price'},text=True)
            loaded=True
        except:
            print('waiting for page to load')
            time.sleep(0.5)
        prices=[]
        try:
            "the following is kinda buggy so almost never gets executed must figure out for the future"
            reserved=soup.findAll('div',attrs={'class':'reserved-product'})
            for i in range(len(reserved)):    
                product_img=reserved[i].find_element_by_xpath('.//ancestor::div')
                product=product_img.find_element_by_class_name('product')
                price=product.find('div',attrs={'class':'product-price'},text=True)
                print(price)
                prices.append(price)
                reserved=True
            time.sleep(2)

        except:
            prices=soup.findAll('div',attrs={'class':'product-price'},text=True)
            reserved=False    
    for i in range(len(prices)):
        prices[i]=float(re.sub(r',','',prices[i].text.strip()))
    
    average=0
    for i in range(len(prices)):
        average+=prices[i]/len(prices)
    if(reserved==True):
        print( 'the average price of reserved price in the Korean market is '+ str(math.ceil(average))+' KRW')
    else:
        print( 'the average price in the Korean market is '+ str(math.ceil(average))+' KRW')
    while(True):
        pass
    #wait(driver, 15).until_not(EC.title_is(title))

if __name__ == "__main__":
    #getData(sys.argv[1])
    getData("이지 부스트 750")
