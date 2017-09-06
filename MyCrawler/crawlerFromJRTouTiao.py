#coding=utf-8
'''
Created on 2017-09-04
根据链接爬取今日头条的文本内容，爬取文章的标题，内容，摘要。
article:
  id,
  title,标题
  content,内容
  abstract,摘要
  name,来源
  chineseTag,分类
@author: wenhaohu
'''
import urllib
from bs4 import BeautifulSoup
import json
import re

# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

invalid_escape = re.compile(r'\\[0-7]{1,3}')  # up to 3 digits for byte values up to FF

def replace_with_byte(match):
    return chr(int(match.group(0)[1:], 8))

def repair(brokenjson):
    return invalid_escape.sub(replace_with_byte, brokenjson)        

"""
根据url获取今日头条的文章等信息，有些字符还是无法去除干净，
"""
def getArticleFromUrl(url):
    try:
        resp = urllib.request.urlopen(url)
    except Exception:
        print('url open error')
        return None
    respHtml = resp.read()
    resp.close()
    soup = BeautifulSoup(respHtml,from_encoding="utf-8")
    content='null'
    scripts = soup.find_all('script')
    for sc in scripts: #sc 是bs4.element.Tag,name是名字，
        line = str(sc)
        if line.startswith('<script>var BASE_DATA ='):
            lineRes = line.replace('<script>var BASE_DATA =', '').replace(';</script>', '').replace('.replace(/<br \/>|\\n|\\r/ig, \'\')', '').replace('.replace(/<br \/>/ig, \'\')', '')
            res = lineRes.replace('    ', '').replace('  ', '')
            vs = res.split('\n')
            chineseTag = vs[14]
            title = vs[19]
            content = re.sub('<[^<]*>|&[a-z]+\073|\/p','',vs[20])
            abstract = vs[33]
    return content    

"""
根据给定的url集合，获取今日头条的文章等信息，
集合从一个txt文件中获得，返回对应的文章等信息，
写入txt文件
"""
def getArticlesFromUrls(urlsPath,savefile):
    f = open(urlsPath,encoding='utf-8')
    save = open(savefile,"a",encoding='utf-8')
    line = f.readline()
    while 1:
        if not line:
            break
        else:
            line = line.replace('\n','')
            content = getArticleFromUrl(line)
            if content is not None:
                res = (line+'\t'+content).replace('\u200d','').replace('\xa3','').replace('\ue20c','')
            else:
                res = line+'\t'+'null'
            #得到内容写进txt文件
            save.write(res+'\n')
            line = f.readline()
    save.close()

#根据url集合获得文章信息
urlsPath=r'E:\workspace\data\JRtoutiaoArticle\urls.txt'
savefile=r'E:\workspace\data\JRtoutiaoArticle\urls_articles.txt'
  
getArticlesFromUrls(urlsPath,savefile)

# print(getArticleFromUrl('http://www.toutiao.com/a6459893669330682381'))







