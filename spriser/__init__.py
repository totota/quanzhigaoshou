#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from chirp.ui.config import get
from selenium.webdriver.support.ui import WebDriverWait

quanzhigaoshou=u''
mainurl='http://www.xinshubao.net/15/15209/'
cout=0
def looknext(cout,quanzhigaoshou,sourcehtmlurl):
    cout=cout+1
    print cout
    driver=webdriver.PhantomJS(executable_path='/root/tool/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    driver.get(sourcehtmlurl)
    WebDriverWait(driver,10).until(lambda x:x.find_element(By.ID,'content'))
    WebDriverWait(driver,10).until(lambda x:x.find_element(By.CLASS_NAME,'fye2'))
    quanzhigaoshou = quanzhigaoshou+driver.find_element_by_id('content').text
    bsobj=BeautifulSoup(driver.page_source)
    driver.close()
    links=bsobj.findAll('a')
    nextpage=u'下一章'
    #print nextpage
    for link in links:
        if 'href' in link.attrs:
            linktext=unicode(link.string)
            if linktext==nextpage:
                print link.attrs['href']
                if link.attrs['href']=='./':
                    #print quanzhigaoshou
                    return quanzhigaoshou,'ok'
                else:
                    if cout==100:
                        cout=0
                        nextsourcehtmlurl=mainurl+link.attrs['href']
                        print nextsourcehtmlurl
                        return quanzhigaoshou,nextsourcehtmlurl
                    nextsourcehtmlurl=mainurl+link.attrs['href']
                    newquanzhigaoshou,ok = looknext(cout,quanzhigaoshou,nextsourcehtmlurl)
                    if ok!='ok':
                        print newquanzhigaoshou
                        return newquanzhigaoshou,ok
                    return newquanzhigaoshou,'ok'
print 'start...........'
straturl='http://www.xinshubao.net/15/15209/1489658.html'
f=open('/root/text.txt','r+')
while straturl !='ok':
    print straturl
    print quanzhigaoshou
    quanzhigaoshou,straturl=looknext(cout,quanzhigaoshou,straturl)
    quanzhigaoshou1='''
    '''+quanzhigaoshou.encode('utf-8')
    f.write(quanzhigaoshou1)
    quanzhigaoshou=u''
    print straturl
f.close()






