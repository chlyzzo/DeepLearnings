#coding=utf-8
'''
Created on 2018-01-19

@author: wenhaohu

http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
周边检索详见参数

秘钥=6OOOB36qGtsQZWOKXGgkAH8AQuux11YG

'''

import urllib
import json
import time
from bs4 import BeautifulSoup

noResultfilePath='/home/min/workspace/data/spiderDataSet/no_vppv_comm_baidu_corpus/noresult_comm_baidu_mess.txt'


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
去除掉换行符，用在一行的最后
'''
def replacenNewlineChar(inputStr):
    newStr = inputStr.replace('\r\n','').replace('\r','').replace('\n','')
    return newStr   

'''
读取小区的经纬度等信息，获取小区的附近数据点，
comm_id,lat,lng,queryWord,

'ak=DqBFd4FXWonuaMNfGDRU0eEm',
'ak=vj0goyn1bffZwsjk3C8KH3G9',

'''
def readCommLatLngGetBaiduMess(file,saveFile):
        
    keys = ['ak=********']
    key = keys[0]
    akLen = len(keys)
    useAKKEYID = 1
    f = open(file,'r',encoding='utf-8')
    line = f.readline()
    vs = line.split('\t')
    while 1:
        if line is not None and len(vs)==4:
            commId = replacenNewlineChar(vs[0])
            lat = replacenNewlineChar(vs[2])
            lng = replacenNewlineChar(vs[3])
            print(commId+' start')
            #所有类别遍历查询
            for label in allLabels:
                listMap = getListMapMessByCommMess(commId,lat,lng,label,key)#获得信息
                #判断获得的数据是否正确，即是否超量，
                if (listMap=='error'):
                    print(label+'error')
                elif (listMap=='302'):#判断key的使用是否超量
                    print('超限')
                    if (useAKKEYID<akLen):
                        key = keys[useAKKEYID]
                        useAKKEYID = useAKKEYID + 1#ak用的后移一个
                    else:
                        return 'error'
                elif (listMap is None or len(listMap)<1):
                    print(label+' read mess is None')
                else:
                    outResult = getOneListMapToSting(listMap,label)#返回信息格式处理
                    appendWriteCommDataBase(outResult,commId,saveFile)#结果写进保存文件中
                time.sleep(0.001)
            #下一个小区
            print(commId+' end')
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
MpZvU6f5YAv7P6jqu5FAyaoDmWSx0Hhw
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
#         soup = BeautifulSoup(respHtml,from_encoding="utf-8")
#         result = str(soup).replace('<html><body><p>','').replace('</p></body></html>','')
        #判断返回的值是否正确，如果是限量则换一个key，如果是其他报错，则直接退出
        returnJson = json.loads(respHtml)
        if (returnJson.get('status',None)==302):
            writeNoResultIntoTxt(commId,lat,lng,label)
            return '302'
        elif (returnJson.get('message',None)!='ok'):
            writeNoResultIntoTxt(commId,lat,lng,label)
            return 'error'   

    except urllib.error.URLError:
        #url获取错误
        time.sleep(0.2)#休息20秒
    except Exception:
        #其他异常
        time.sleep(0.1)#休息20秒      
    #json串转成List[Map[]]
    listMap = returnJson.get('results',None)
    #如果没有获取到数据，则额外存储该小区，待后续再查
    if listMap is None or len(listMap)<1 :
        writeNoResultIntoTxt(commId,lat,lng,label)
    return listMap


'''
未找到的写进noresult-text里
'''                
def writeNoResultIntoTxt(commId,lat,lng,label):
    with open(noResultfilePath,'a',encoding='utf-8') as f:
            f.write(str(commId)+'\t'+str(lat)+'\t'+str(lng)+'\t'+label+'\r\n') 
    

#-------------------------------------------------------------------

'''
主函数开始
'''
                
# file = 'D:/comm_baidu_corpus/input_comm_lat_lng_7.txt'
# saveFile = '/home/min/workspace/data/spiderDataSet/output_comm_baidu_mess.txt'
# start = 120
# endFile = 165
# while (start<=endFile):
#     file = '/home/min/workspace/data/spiderDataSet/comm_baidu_corpus/input_comm_lat_lng_'+str(start)+'.txt'
#     print(file)
#     oneFindStatus = readCommLatLngGetBaiduMess(file,saveFile,'银行')  
#     print(file+'....'+'end search.')  
#     if (oneFindStatus=='ok'):
#         start = start + 1
#     else:
#         print('error at=')
#         print(file)
#         break
saveFile = '/home/min/workspace/data/spiderDataSet/no_vppv_comm_baidu_corpus/no_vppv_comm_lat_lng_splits_messout/no_vppv_comm_lat_lng_totle_mess'
file = '/home/min/workspace/data/spiderDataSet/no_vppv_comm_baidu_corpus/no_vppv_comm_lat_lng_totle'
oneFindStatus = readCommLatLngGetBaiduMess(file,saveFile)  

