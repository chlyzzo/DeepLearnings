#coding=utf-8
'''
Created on 2018-01-19

@author: wenhaohu

http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
周边检索详见参数

秘钥=6OOOB36qGtsQZWOKXGgkAH8AQuux11YG

'''

import urllib
from bs4 import BeautifulSoup
import json
import time

noResultfilePath='d:/noresult_comm_baidu_mess.txt'

'''
返回的值串：
百度返回的数据ListMap解析成Array[String]
'''
def getOneListMapToSting(listMap,label):
    result = []
    if listMap is not None:
        for map in listMap:
            location = map.get('location','{}')
            lat = location.get('lat','0')
            lng = location.get('lng','0')
            uid = map.get('uid','default')
            name = map.get('name','default')
            address = map.get('address','default')
            detail = map.get('detail','default')
            street_id  = map.get('street_id','0') #默认值
            #组合结果输出
            line = uid+'\t'+name+'\t'+street_id+'\t'+str(lat)+'\t'+str(lng)+'\t'+address+'\t'+str(detail)+'\t'+label
            result.append(line)
        #所有元素
    return result


'''
array[String]写数据进表里，一个小区多条，即一个小区多行，写文件是追加的写,

f=open('路径/文件名', '读写格式', '编码方式', '错误处理方式')

'''    

def appendWriteCommDataBase(arrayString,comm_id,filePath):
    if arrayString is not None:
        for oneData in arrayString:
            writeLine = str(comm_id)+'\t'+oneData+'\r\n'
            with open(filePath,'a',encoding='utf-8') as f:  
                f.write(writeLine)  


'''
读取小区的经纬度等信息，获取小区的附近数据点，
comm_id,lat,lng,queryWord,

'''
def readCommLatLngGetBaiduMess(file,saveFile,label):
    f = open(file,'r',encoding='utf-8')
    line = f.readline()
    vs = line.split('\t')
    while 1:
        if line is not None and len(vs)==4:
            commId = vs[0]
            lat = vs[2]
            lng = vs[3]
            listMap = getListMapMessByCommMess(commId,lat,lng,label)#获得信息
            outResult = getOneListMapToSting(listMap,label)#信息格式处理
            appendWriteCommDataBase(outResult,commId,saveFile)#写进保存文件中
            time.sleep(2)
            line = f.readline()
            vs = line.split('\t')
        else:
            break   
         
    f.close()              

'''
根据一个小区的经纬度信息，爬取其周边指定的标签数据
返回一个listMap

query=银行$酒店，查询地点关键字
http://lbsyun.baidu.com/index.php?title=lbscloud/poitags

tag=一级行业分类，二级行业分类，
ak
pKx1umPLme6VloE24RirnXiS3tPfba4O
vj0goyn1bffZwsjk3C8KH3G9
DqBFd4FXWonuaMNfGDRU0eEm
DD279b2a90afdf0ae7a3796787a0742e
'''    
def getListMapMessByCommMess(commId,lat,lng,label):
    key='ak=DqBFd4FXWonuaMNfGDRU0eEm'
    #url查询
    location='location='+str(lat)+','+str(lng)
    queryPath = 'http://api.map.baidu.com/place/v2/search?radius=2000&output=json'
    queryUrlCode = urllib.parse.quote(label) #编码url形式
    query = queryPath+'&'+'query='+queryUrlCode+'&'+key+'&'+location
    result='{}'
    try:
        resp = urllib.request.urlopen(query)
        respHtml = resp.read().decode('utf-8')
        resp.close()
        soup = BeautifulSoup(respHtml,from_encoding="utf-8")
        result = str(soup).replace('<html><head></head><body>','').replace('</body></html>','')
        print(result)
    except urllib.error.URLError:
        #url获取错误
        time.sleep(20)#休息20秒
    except Exception:
        #其他异常
        time.sleep(10)#休息20秒      
    #json串转成List[Map[]]
    listMap = json.loads(result).get('results',None)
    #如果没有获取到数据，则额外存储该小区，待后续再查
    if listMap is None:
        with open(noResultfilePath,'a',encoding='utf-8') as f:  
            f.write(str(commId)+'\t'+str(lat)+'\t'+str(lng)+'\n')  
    return listMap
                
#-------------------------------------------------------------------

'''
主函数开始
'''
file = 'd:/input_comm_lat_lng.txt'
saveFile = 'd:/output_comm_baidu_mess.txt'
readCommLatLngGetBaiduMess(file,saveFile,'银行')



