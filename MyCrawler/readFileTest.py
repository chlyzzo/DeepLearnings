#coding=utf-8
'''
Created on 2017-09-05

@author: wenhaohu
'''

# f= open(r'E:\workspace\data\JRtoutiaoArticle\urls_articles.txt',encoding='utf-8')
# line = f.readline()
# while 1:
#     if not line:
#         break
#     else:
#         print(line)
#         line = f.readline()

'''
python获取一个目录下的所有文件
'''
import os        
dirPath = 'D:\comm_baidu_corpus' 
files = os.listdir(dirPath)

for file in files:
    print(dirPath+"\\"+file)



