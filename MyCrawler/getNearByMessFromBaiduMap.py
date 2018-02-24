#coding=utf-8
'''
Created on 2018-01-19

@author: wenhaohu

http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
周边检索详见参数


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
        
    keys = ['ak=*****']
    key = keys[0]
    akLen = len(keys)
    useAKKEYID = 1
    f = open(file,'r',encoding='utf-8')
    line = f.readline()
    vs = line.split('\t')
    while 1:
        if line is not None and len(vs)==4:
            commId = vs[0]
            lat = vs[2]
            lng = vs[3]
            listMap = getListMapMessByCommMess(commId,lat,lng,label,key)#获得信息
            #判断获得的数据是否正确，即是否超量，
            if (listMap=='error'):
                print('error')
                return 'error'
            elif (listMap=='302'):#判断key的使用是否超量
                print('超限')
                if (useAKKEYID<akLen):
                    key = keys[useAKKEYID]
                    useAKKEYID = useAKKEYID + 1#ak用的后移一个
                else:
                    return 'error'
            else:
                outResult = getOneListMapToSting(listMap,label)#信息格式处理
                appendWriteCommDataBase(outResult,commId,saveFile)#写进保存文件中
            time.sleep(1)
            line = f.readline()
            vs = line.split('\t')
        else:
            break   
         
    f.close()
    return 'ok'              

'''
根据一个小区的经纬度信息，爬取其周边指定的标签数据
返回一个listMap

query=银行$酒店，查询地点关键字
http://lbsyun.baidu.com/index.php?title=lbscloud/poitags

tag=一级行业分类，二级行业分类，
ak
pKx1umPLme6VloE24RirnXiS3tPfba4O
vj0goyn1bffZwsjk3C8KH3G9,可用
DqBFd4FXWonuaMNfGDRU0eEm，可用
'''    
def getListMapMessByCommMess(commId,lat,lng,label,akkey):
    #url查询
    location='location='+str(lat)+','+str(lng)
    queryPath = 'http://api.map.baidu.com/place/v2/search?radius=2000&output=json'
    queryUrlCode = urllib.parse.quote(label) #编码url形式
    query = queryPath+'&'+'query='+queryUrlCode+'&'+akkey+'&'+location
    returnJson=json.loads('{}')
    try:
        resp = urllib.request.urlopen(query)
        respHtml = resp.read().decode('utf-8')
        resp.close()
        soup = BeautifulSoup(respHtml,from_encoding="utf-8")
        result = str(soup).replace('<html><head></head><body>','').replace('</body></html>','')
        #判断返回的值是否正确，如果是限量则换一个key，如果是其他报错，则直接退出
        returnJson = json.loads(result)
        print(commId)
        if (returnJson.get('status',None)==302):
            return '302'
        elif (returnJson.get('message',None)!='ok'):
            return 'error'   

    except urllib.error.URLError:
        #url获取错误
        time.sleep(20)#休息20秒
    except Exception:
        #其他异常
        time.sleep(10)#休息20秒      
    #json串转成List[Map[]]
    listMap = returnJson.get('results',None)
    #如果没有获取到数据，则额外存储该小区，待后续再查
    if listMap is None:
        with open(noResultfilePath,'a',encoding='utf-8') as f:  
            f.write(str(commId)+'\t'+str(lat)+'\t'+str(lng))  
    return listMap
                
#-------------------------------------------------------------------

'''
主函数开始
'''
# file = 'D:/comm_baidu_corpus/input_comm_lat_lng_7.txt'
saveFile = 'd:/output_comm_baidu_mess.txt'
start = 15
endFile = 165
while (start<=endFile):
    file = 'D:/comm_baidu_corpus/input_comm_lat_lng_'+str(start)+'.txt'
    print(file)
    oneFindStatus = readCommLatLngGetBaiduMess(file,saveFile,'银行')  
    print(file+'....'+'end search.')  
    if (oneFindStatus=='ok'):
        start = start + 1
    else:
        print('error at=')
        print(file)
        break
