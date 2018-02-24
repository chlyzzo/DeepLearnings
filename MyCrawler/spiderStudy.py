#coding=utf-8
'''
Created on 2018-01-27

@author: wenhaohu

正则爬取网站信息，
http://www.doutula.com/photo/list/

'''
import urllib
from bs4 import BeautifulSoup
import json
import time
import re
import random
import time
#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 



'''
正则解析出这些值
data-original="http://ww3.sinaimg.cn/bmiddle/9150e4e5ly1fnty5s6wqzj205005mjrc.jpg" alt="吸猫女大佬"
把需要提取出的用括号，转变成，
data-original="(.*?)" .*?alt="(.*?)"
''' 

'''
连接数据库
import pymysql

db = pymysql.connect{
    host = '',
    port = '',
    user = '',
    password = '',
    db = '',
    charset='utf-8'
}

游标
cursor = db.cursor()

插入数据
cursor.execute("insert into image(`name`,`url`) values(
'{}','{}')".format(i[1],i[0]))
db.commit()
db.close()

'''
filePath = 'd:/spider_data_output.txt'
user_agents = [  
    'Opera/9.25 (Windows NT 5.1; U; en)',  
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',  
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',  
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",  
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",  
] 
def getImagesList(page=1):
    query = 'http://www.doutula.com/photo/list/?page={}'.format(page)
    headers = {}
    headers['User-Agent']=random.choice(user_agents)
    resp = urllib.request.Request(url=query,headers=headers)
    respHtml = urllib.request.urlopen(resp).read().decode('utf-8')
    respHtml = respHtml.replace('\r\n','').replace('\n','')
    reg = r'data-original="(.*?)" .*?alt="(.*?)"'
    reg = re.compile(reg, re.S)#正则元组，正则有两个提取元素，两个括号匹配的，
    imageslist = re.findall(reg,respHtml)#返回数组
    #数据进行保存
    for i in imageslist:
        # i=(url,name)
        line = i[1]+'\t'+i[0]+'\n'
        with open(filePath,'a',encoding='utf-8') as f:  
                f.write(line) 
  

for i in range(1,1004):      
    print("正在爬取第{}页数据.".format(i))
    time.sleep(2)
    getImagesList(i)





