
# coding: utf-8

# # post 資料準備

# In[8]:

import requests
from bs4 import BeautifulSoup as bs
import re
import time
url ='http://www.cht.com.tw/portal/Location_query'
payload = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
"Cache-Control":"max-age=0",
"Content-Length":"141",
"Content-Type":"application/x-www-form-urlencoded",
"Cookie":"JSESSIONID=FD9C791F0EAEB7DC58C68852072E4E1E; wb48617274=5993CFE0; va-dtid=1473140492149; __utmt=1; _dc_gtm_UA-63432891-1=1; __atuvc=3%7C36; __atuvs=57ce570b1d01eecd002; __utma=66575100.586797246.1473140492.1473140492.1473140492.1; __utmb=66575100.3.10.1473140492; __utmc=66575100; __utmz=66575100.1473140492.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.3.586797246.1473140492",
"Host":"www.cht.com.tw",
"Origin":"http://www.cht.com.tw",
"Proxy-Connection":"keep-alive",
"Referer":"http://www.cht.com.tw/portal/Location_query",
"Upgrade-Insecure-Requests":"1",
"cate":"1",
"counCode":"0",
"townCode":"00",
"currentpage1":"0",
"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"}


# # helper function 

# In[41]:

# 正規表達式挑出數字
def numberCleaner(st):
    match = re.search(r'[\d,]+',st)
    num = int(match.group().encode('utf-8'))
    return  num

# 挑選需要的網頁資料
def contentCrawler(soup):
    nameList=soup.select('.in-services-title')
    dataform = soup.select('.services-result div table')
    count = 0
    result = []
    for table in dataform:        
        name=nameList[count].text
        address = table.select('.address')        
        tel = table.select('td')
        #print (tel[1].text.strip())
        result.append(name+','+address[0].text.strip()+','+tel[1].text.strip()+'中華電信')
        count = count +1
        
    return result


# In[43]:

res = requests.post(url , data = payload)
soup = bs(res.text)
# 抓第一次以後決定總頁數
page = soup.select('.pager-total')[0].text
page=numberCleaner(page)

# 爬取所有資料存成list
for i in range(0,page):
    payload['currentpage1']=str(i)
    res = requests.post(url , data = payload)
    soup = bs(res.text)
    result=result+contentCrawler(soup)    
    time.sleep(0.5)


# # 寫入檔案

# In[45]:

with open('cht.txt','w',encoding='utf-8') as f:
    for line in result:
        f.write(line+'\n')

