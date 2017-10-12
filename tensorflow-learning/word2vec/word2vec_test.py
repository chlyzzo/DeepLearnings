#coding=utf-8
'''
Created on 2017-09-27

@author: wenhaohu
'''
from process_data import build_vocab
from process_data import convert_words_to_index
from process_data import generate_sample

words = ('a','a','b','c','b','c','d','e')#读取训练所有词，存储在一个list中，
dictionary, _ = build_vocab(words, 20)#建立词典，根据指定的词典大小，词典的构建依赖于词在训练样本中的频率
index_words = convert_words_to_index(words, dictionary)#得到词典，把训练集替换成索引，即文字-->数字
del words # 词存入内存
single_gen = generate_sample(index_words, 2)

print(dictionary)
print(index_words)

for i in range(100):
   center,target=next(single_gen)
   print(str(center)+"="+str(target))

