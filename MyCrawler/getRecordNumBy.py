#coding=utf-8
'''
Created on 2018-02-07

@author: wenhaohu
'''

import urllib
from bs4 import BeautifulSoup
import json
import time
import re
import random
import time



query = 'http://tjtx-98-28.58os.org:8042/node/containerlogs/container_e10_1509011180094_16205765_01_000760/hdp_anjuke_bi/syslog/?start=0'
resp = urllib.request.Request(url=query)
respHtml = urllib.request.urlopen(resp).read().decode('utf-8')

reg = r'dmg_hwh_oversea_loupan_sim_a_base/(.*?).lzo for a'
reg = re.compile(reg, re.S)
fileName = re.findall(reg,respHtml)
reg2 = r'RECORDS_OUT_1_hdp_anjuke_dw_db_temp.dmg_hwh_oversea_sim_smb_data:(\d+)'
reg2 = re.compile(reg2, re.S)#正则元组，正则有两个提取元素，两个括号匹配的，
record = re.findall(reg2,respHtml)#返回数组

print(fileName,record)
