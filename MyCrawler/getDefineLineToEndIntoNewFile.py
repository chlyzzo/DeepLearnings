#coding=utf-8
'''
Created on 2018-01-19

@author: wenhaohu

'''

filePath='/home/min/workspace/data/spiderDataSet/input_comm_lat_lng_backup.txt'
saveFile = '/home/min/workspace/data/spiderDataSet/input_comm_lat_lng.txt'

def readCommLatLngGetBaiduMess(file):
      
    f = open(file,'r',encoding='utf-8')
    line = f.readline()
    count=1
    while 1:
        if line is not None :
            if count>=282797:
               writeResultIntoTxt(line,saveFile)
            line = f.readline()
            count = count + 1
        else:
            break   
         
    f.close()

'''
未找到的写进noresult-text里
'''                
def writeResultIntoTxt(line,saveFile):
    with open(saveFile,'a',encoding='utf-8') as f:  
            f.write(line)  
    
readCommLatLngGetBaiduMess(filePath)





