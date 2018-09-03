import urllib,urllib3, json, re,requests,time
from rauth import OAuth2Service
from sentiment import *
from urllib.parse import quote, parse_qs
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
def function():
    baseurl = "https://accounts.google.com/o/oauth2/v2/auth?"
    googlefilename='client_secret.json'
    google=jd(googlefilename)
    #yql_query = "select wind from weather.forecast where woeid=2460286"
    #put the 'q' on top for regex reasons
    headers={
        'scope' : 'https://www.googleapis.com/auth/youtube.readonly',
        'redirect_uri' : google['web']['redirect_uris'][0],
        'include_granted_scopes':'true',
        'response_type' : 'token',
        'client_id':google['web']['client_id']
    }
    """
    token=jd('localInfo.json')['bearertoken']
    headers={
        'q':yql_query,
        'format':'json',
        'Authorization':'Bearer '+token
    }
    """
    urladd=''
    first_index=True
    for key in headers:
        #value=headers[key].replace("\:",r'%3A')
        value=quote(headers[key])
        #print(value)
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
    from selenium import webdriver
    pathtocdriver = "C:\SDKs\seleniumdriver\chromedriver.exe"
    driver=webdriver.Chrome(pathtocdriver)
    driver.get(url)
    googleid=jd('localInfo.json')['gmailid']
    googlepw=jd('localInfo.json')['gmailpassword']
    oldtitle=driver.title
    newtitle=driver.title
    logged_in=False
    profile_selected=False
    #print(url)
    while (True):
        newtitle = driver.title
        try:
            profile=driver.find_element_by_xpath("//*[contains(text(), 'Bernard Ahn')]")
            profile.click()
            time.sleep(5)
        except:
            pass
        
        try:
            oldhead=driver.find_element_by_id("headingText")
            newhead=driver.find_element_by_id("headingText")
            emailelem = driver.find_element_by_xpath("//input[@type='email']")
            emailelem.send_keys(googleid)
            idbuttonelem = driver.find_element_by_id("identifierNext")
            idbuttonelem.click()
            while(oldhead==newhead):
                newhead=driver.find_element_by_id("headingText")
            try:
                elem = driver.find_element_by_xpath("//input[@type='password']")
                elem.send_keys(googlepw)
                elem = driver.find_element_by_id("passwordNext")
                elem.click()
                time.sleep(5)
            except:
                pass 
        except:
            pass
        """
        newtitle=driver.title
        if(newtitle is not oldtitle):
            logged_in=True
        """
        if(driver.title=='squwbs'):
            print (parse_qs(driver.current_url))
            driver.quit()
            #wait(driver, 15).until_not(EC.title_is(title))

if __name__ == "__main__":
    function()