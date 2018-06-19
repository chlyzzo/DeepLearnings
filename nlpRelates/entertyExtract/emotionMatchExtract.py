#coding=utf-8
'''
Created on 2018-06-19
@author: wenhaohu
情感搭配抽取，
1，对象，2，观点词
2，排序，3，语义相似挑选
'''
import jieba

trs = jieba.cut("说电话反馈是斯蒂芬斯")
for tr in trs:
    print(tr)



