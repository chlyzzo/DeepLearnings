#coding=utf-8
'''
Created on 2018-01-30

@author: wenhaohu

切分文件，给定指定的行数

'''
import math
lines = 33000
file = 'd:/input_comm_lat_lng.txt'
f = open(file,'r',encoding='utf-8')
line = f.readline()
count =1
while 1:
    if line is not None and len(line)>4:
        newFileName = 'd:/comm_baidu_corpus/input_comm_lat_lng'+"_"+str(math.ceil(count/lines))+'.txt'
        vs = line.split('\t')
        if (vs[0]>'0'):
            with open(newFileName,'a',encoding='utf-8') as fwrite:  
                fwrite.write(line)  
            count = count + 1
        line = f.readline()
    else:
        break
f.close()













