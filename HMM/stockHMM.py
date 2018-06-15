#coding=utf-8
'''
Created on 2018-06-15

@author: wenhaohu
股票预测，使用HMM，

'''
import numpy as np
from hmmlearn import hmm
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings

def expand(a,b):
    d = (b-a) * 0.05
    return a-d,b+d

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    
    # 0日期  1开盘  2最高  3最低  4收盘  5成交量  6成交额
    # 每行\t分割，从第三行开始读取，取的列顺序是4,5,6,2,3
    x = np.loadtxt("26.SH600000.txt",delimiter='\t', skiprows=2, usecols=(4, 5, 6, 2, 3))
    close_price = x[:,0] #收盘
    volumn = x[:,1]#成交量
    amount = x[:,2]#成交额
    amplitude_price = x[:,3]-x[:,4] #每天的最高价与最低价差
    diff_price = np.diff(close_price) #涨跌值
    print(np.shape(volumn))
    volumn = volumn[1:]  # 成交量
    amount = amount[1:]  # 成交额
    amplitude_price = amplitude_price[1:] # 每日振幅
    #涨跌值，成交量，成交额，每日振幅，
    sample = np.column_stack((diff_price, volumn, amount, amplitude_price)) # 观测值
    n = 5
    model = hmm.GaussianHMM(n_components=n,covariance_type='full')
    model.fit(sample)
    y = model.predict_proba(sample)
    np.set_printoptions(suppress=True)
    print(y)
    
    t = np.arange(len(diff_price))
    mpl.rcParams['font.sans-serif']=[u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10,8), facecolor='w')
    plt.subplot(421)
    plt.plot(t, diff_price, 'r-')
    plt.grid(True)
    plt.title(u'涨跌幅')
    plt.subplot(422)
    plt.plot(t, volumn, 'g-')
    plt.grid(True)
    plt.title(u'交易量')

    clrs = ['b','g','r','c','m']
    plt.subplot(423)
    for i, clr in enumerate(clrs):
        plt.plot(t, y[:, i], '-', color=clr, alpha=0.7)
    plt.title(u'所有组分')
    plt.grid(True)
    for i, clr in enumerate(clrs):
        axes = plt.subplot(4, 2, i+4)
        plt.plot(t, y[:, i], '-', color=clr)
        plt.title(u'组分%d' % (i+1))
        plt.grid(True)
    plt.suptitle(u'SH600000股票：GaussianHMM分解隐变量', fontsize=18)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()
