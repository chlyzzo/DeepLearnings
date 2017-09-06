#coding=utf-8
'''
Created on 2017-09-05

@author: wenhaohu
'''

f= open(r'E:\workspace\data\JRtoutiaoArticle\urls_articles.txt',encoding='utf-8')
line = f.readline()
while 1:
    if not line:
        break
    else:
        print(line)
        line = f.readline()


