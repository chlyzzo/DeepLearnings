#coding=utf-8
'''
Created on 2018-06-06

@author: wenhaohu

使用synonyms，去近义词或者语义相同的词

使用的技术：word2vec计算语义相似度；
使用编辑距离计算两个词的相似度；

'''
import synonyms

#展示近义词，调试用
synonyms.display("楼盘")

#计算指定的两个词近似度
#默认对输入的两个待计算串进行分词
r = synonyms.compare("你好明天", "明天很不好", seg=True)
print(r)

#计算某个词的近词，list返回
wordSimList = synonyms.nearby("美铝")
print(wordSimList)





