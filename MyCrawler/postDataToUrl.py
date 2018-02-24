#coding=utf-8
'''
Created on 2018-02-05

@author: wenhaohu
'''
#coding=utf-8
import urllib
from urllib import parse
from urllib import request
data={}
data['bizId']=13
data['field']='qatitle'
data['text']='时间放开第三方'

headers = {}
headers['Content-Type']={'application/json; charset=utf8'}
query = 'http://banword.a.ajkdns.com/singlematch/?bizId={0}&field={1}&text={2}'.format(data['bizId'],data['field'],data['text'])
headers = {}
headers['Content-Type']={'application/json; charset=utf8'}
resp = urllib.request.Request(url=query,headers=headers)
respHtml = urllib.request.urlopen(resp).read()
print(respHtml)



