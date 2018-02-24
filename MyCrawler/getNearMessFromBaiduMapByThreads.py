#coding=utf-8
'''
Created on 2018-02-23

@author: wenhaohu

多线程爬取百度地图信息，每个线程爬取一个类，

设置10个线程，原始的小区信息分成10份；每一份的小区爬取全部的类别（123个）


'''

import urllib
from bs4 import BeautifulSoup
import json
import time
import os

noResultfilePath='d:/noresult_comm_baidu_mess.txt'

#所有的类别，每个小区周边的所有信息
allLabels = ['中餐厅','外国餐厅','小吃快餐店','蛋糕甜品店','咖啡厅','茶座','酒吧',
 '星级酒店','快捷酒店','公寓式酒店',
 '购物中心','超市','便利店','家居建材','家电数码','商铺','集市',
 '通讯营业厅','邮局','物流公司','售票处','洗衣店','图文快印店','照相馆','房产中介机构','公用事业','维修点','家政服务','殡葬服务','彩票销售点','宠物服务','报刊亭','公共厕所',
 '美容','美发','美甲','美体 ',           
 '公园','动物园','植物园','游乐园','博物馆','水族馆','海滨浴场','文物古迹','教堂','风景区',
 '度假村','农家院','电影院','KTV','剧院','歌舞厅','网吧','游戏场所','洗浴按摩','休闲广场',        
 '体育场馆','极限运动场所','健身中心',
 '高等院校','中学','小学','幼儿园','成人教育','亲子教育','特殊教育学校','留学中介机构','科研机构','培训机构','图书馆','科技馆',        
 '新闻出版','广播电视','艺术团体','美术馆','展览馆','文化宫',          
 '综合医院','专科医院','诊所','药店','体检机构','疗养院','急救中心','疾控中心',     
 '汽车销售','汽车维修','汽车美容','汽车配件','汽车租赁','汽车检测场',
 '飞机场','火车站','地铁站','长途汽车站','公交车站','港口','停车场','加油加气站','服务区','收费站','桥',
 '银行','ATM','信用社','投资理财','典当行',
 '写字楼','住宅区','宿舍',
 '公司','园区','农林园艺','厂矿',
 '中央机构','各级政府','行政单位','公检法机构','涉外机构','党派团体','福利机构','政治教育机构'
             ]

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
comm_id,lat,lng,queryWord

一个线程的操作，一份小区信息，结果文件，线程名字即读入的文件名字，

'''
def readCommLatLngGetBaiduMess(file,saveFile):
        
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
            #所有类别遍历查询
            for label in allLabels:
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
                    outResult = getOneListMapToSting(listMap,label)#返回信息格式处理
                    appendWriteCommDataBase(outResult,commId,saveFile)#结果写进保存文件中
                time.sleep(1)
            #下一个小区
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
            writeNoResultIntoTxt(commId,lat,lng)
            return '302'
        elif (returnJson.get('message',None)!='ok'):
            writeNoResultIntoTxt(commId,lat,lng)
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


'''
未找到的写进noresult-text里
'''
def writeNoResultIntoTxt(commId,lat,lng):
    with open(noResultfilePath,'a',encoding='utf-8') as f:
            f.write(str(commId)+'\t'+str(lat)+'\t'+str(lng))


#=====================================
'''
线程初始化，

'''
import threading

class myThread (threading.Thread):
    def __init__(self, threadID, dirPath,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.dirPath = dirPath
        
    def run(self):
        print ("开始线程：" + self.name)
        getFileCommNearMessThread(self.dirPath,self.name)
        print ("退出线程：" + self.name)
'''
线程的操作
每一份信息文件进行所有类别的爬取
'''
def getFileCommNearMessThread(dirPath,threadName):
    vs = threadName.split(".")
    saveFile = vs[0]+'_messout'+'.txt'
    readCommLatLngGetBaiduMess(dirPath+'\\'+threadName,dirPath+'\\'+saveFile)
    
                
#-------------------------------------------------------------------
'''
开始主函数获取信息
'''
#1，小区的分信息目录
dirPath = 'D:\comm_baidu_corpus'
files = os.listdir(dirPath)#获取目录下的所有文件

#2，创建线程
thread1 = myThread(1, dirPath,files[0])
thread2 = myThread(2, dirPath,files[1])
thread3 = myThread(3, dirPath,files[2])
thread4 = myThread(4, dirPath,files[3])
thread5 = myThread(5, dirPath,files[4])
thread6 = myThread(6, dirPath,files[5])
thread7 = myThread(7, dirPath,files[6])
thread8 = myThread(8, dirPath,files[7])
thread9 = myThread(9, dirPath,files[8])
thread10 = myThread(10, dirPath,files[9])

#启动线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
thread10.join()

#观察结果
print ("退出主线程")

'''
或者引入线程list
threadList=[]
count = 1
for file in files:
   t=myThread(count,dirPath,file)
   count = count + 1
   threadList.append(t)

for t in threadList:
    t.start()
    
for t in threadList:
    t.join()
    
'''





