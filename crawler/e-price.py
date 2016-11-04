
# coding: utf-8

# In[ ]:

class Requester(object):   
# base class  
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',

    }
    
    def req(self,url):
        connection = True
        import requests
        from bs4 import BeautifulSoup
        import time
        soup=''
        rs = requests.session()
        while connection == True:           
            try:                
                res = rs.get(url,headers=self.headers)
                res.encoding = 'utf-8'
                soup = BeautifulSoup(res.text)                
                connection = False
                
                return soup
            except:
                print ('connection error , sleep 1 min' )                         
                time.sleep(60)


# In[ ]:

def brandCrawler():
    brandLink = []
    domain = 'http://www.eprice.com.tw/'
    rs = Requester()
    soup = rs.req('http://www.eprice.com.tw/mobile/product/')
    for link in soup.select('.manu-block a') :
        brandLink.append(domain + link['href'])
    return brandLink


# In[ ]:

def phoneCrawler(brandList):
    phoneList = []
    rs = Requester()
    domain = 'http://www.eprice.com.tw/'
    for url in brandList:
        soup=rs.req(url)
        for link in soup.select('.prod-detail.normal strong a') :
            if len(link['href']) >2:
                phoneList.append(domain+link['href'])
            else :
                phoneList.append(domain+link['data-url'])
    return phoneList


# In[ ]:


from bs4 import BeautifulSoup
import html5lib 
import pandas as pd
def contentCrawl(url,df = None):
    rs = Requester()
    soup = rs.req(url)
    result = []
    title = []
    name = soup.select('.model span')[0].text
    title.append('name')
    result.append(name)
    for i in range(0,100):
        try :
            white=soup.select('.featurelist .white')[i].text
            gray=soup.select('.featurelist .gray')[i].text
            white_title = white.strip().split('\n')[0]
            white_content = ' '.join(white.strip().split('\n')[1].strip().split('\r'))
            result.append(white_content)
            title.append(white_title)
            gray_title = gray.strip().split('\n')[0]
            gray_content = ' '.join(gray.strip().split('\n')[1].strip().split('\r'))
            title.append(gray_title)
            result.append(gray_content)
        except IndexError :        
            break
    if df is None:
        df = pd.DataFrame(columns=title )
        print('create df !')
        return df
    df.loc[len(df)]=result
    return df
# pd.read_html('http://www.eprice.com.tw/mobile/intro/c01-p5438-samsung-galaxy-s7-edge-32gb/' , attrs={'class':'featurelist'})


# In[ ]:

brandList = brandCrawler()
phoneList=phoneCrawler(brandList)


# In[ ]:

import numpy as np
import time 
count = 0
pdf=contentCrawl(phoneList[0])
for link in phoneList:
    pdf=contentCrawl(link,pdf)
    if count % 100 == 0:
        print(round(count/len(phoneList),2)*100 , '%' )
        time.sleep(0.3)
    count +=1
pdf.to_excel('e-price')


# In[ ]:



