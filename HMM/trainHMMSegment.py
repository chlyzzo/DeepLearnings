#coding=utf-8
'''
Created on 2018-06-13

@author: wenhaohu
'''

'''
加载状态先验值，状态转移矩阵，发射矩阵
'''
import numpy as np
import math
import random

def load_train():
    f = open("pi.txt",'r')
    for line in f.readlines():
        pi = list(map(float,line.split(' ')[:-1]))
    f.close()

    f = open("A.txt",'r')
    A = [[] for x in range(4)] # 转移矩阵：B/M/E/S
    i = 0
    for line in f.readlines():
        A[i] = list(map(float,line.split(' ')[:-1]))
        i += 1
    f.close()

    f = open("B.txt",'r')
    B = [[] for x in range(4)]
    i = 0
    for line in f.readlines():
        B[i] = list(map(float,line.split(' ')[:-1]))
        i += 1
    f.close()
    return pi, A, B

'''
维特比算法，
pi状态先验，4*1
A状态转移矩阵,4*4
B发射矩阵，4*65535
'''
def viterbi(pi, A, B, o):
    T = len(o)   # 观测序列，待分词的序列
    delta = [[0 for i in range(4)] for t in range(T)] # 矩阵T*4,即每个字符对应的状态，统计值，
    pre = [[0 for i in range(4)] for t in range(T)]  # 矩阵T*4，字符当前状态下前一个字符对应的状态，是存状态值，
    for i in range(4): #第0个字符的各个状态值=状态先验值+字符到状态统计值
        delta[0][i] = pi[i] + B[i][ord(o[0])] 
    '''
         第二字符的状态，依赖于前一个字符的状态：
           前一个字符-状态数值[4个]+前一个状态[4个]-当前状态=当前字符-当前状态的数值[最大的那个]，
      delta[t][i]=max(delta[t-1][j]+A[j][i]),j是状态标记，取最大值对应的j=j_max
               因此 pre[t][i]=j_max，即当前字符-当前状态的前一个状态是j_max，            
    '''    
    for t in range(1, T):# 字符序列，从第二个字符开始，
        for i in range(4): # 状态集
            #t字符状态i=前一个字符状态
            delta[t][i] = delta[t-1][0] + A[0][i]
            for j in range(1,4):
                vj = delta[t-1][j] + A[j][i] #前一个字符的状态
                if delta[t][i] < vj:
                    delta[t][i] = vj
                    pre[t][i] = j
            delta[t][i] += B[i][ord(o[t])]
    
    decode = [-1 for t in range(T)]  # 待分词的状态序列标记
    q = 0
    for i in range(1, 4):
        if delta[T-1][i] > delta[T-1][q]:
            q = i
    #最后一个字符的状态=q
    decode[T-1] = q
    for t in range(T-2, -1, -1):
        #T-2开始逆序找状态
        q = pre[t+1][q]
        decode[t] = q
    return decode


def segment(sentence, decode):
    N = len(sentence)
    i = 0
    while i < N:  #B/M/E/S
        if decode[i] == 0 or decode[i] == 1:  # Begin
            j = i+1
            while j < N:
                if decode[j] == 2:
                    break
                j += 1
            print (sentence[i:j+1], "|",)
            i = j+1
        elif decode[i] == 3 or decode[i] == 2:    # single
            print (sentence[i:i+1], "|",)
            i += 1
        else:
            print ('Error:', i, decode[i])
            i += 1   

'''
训练参数形式得到pi,A,B
'''
infinite = -(2**31)

def log_normalize(a):
    s = 0
    for x in a:
        s += x
    s = math.log(s)
    for i in range(len(a)):
        if a[i] == 0:
            a[i] = infinite
        else:
            a[i] = math.log(a[i]) - s
                        
def log_sum(a):
    if not a:   # a为空
        return infinite
    m = max(a)
    s = 0
    for t in a:
        s += math.exp(t-m)
    return m + math.log(s)

def calc_alpha(pi, A, B, o, alpha):
    for i in range(4):
        alpha[0][i] = pi[i] + B[i][ord(o[0])]
    T = len(o)
    temp = [0 for i in range(4)]
    del i
    for t in range(1, T):
        for i in range(4):
            for j in range(4):
                temp[j] = (alpha[t-1][j] + A[j][i])
            alpha[t][i] = log_sum(temp)
            alpha[t][i] += B[i][ord(o[t])]
            
    print("alpha end")

def calc_beta(pi, A, B, o, beta):
    T = len(o)
    for i in range(4):
        beta[T-1][i] = 1
    temp = [0 for i in range(4)]
    del i
    for t in range(T-2, -1, -1):
        for i in range(4):
            beta[t][i] = 0
            for j in range(4):
                temp[j] = A[i][j] + B[j][ord(o[t+1])] + beta[t+1][j]
            beta[t][i] += log_sum(temp)
    print("beta end")

def calc_gamma(alpha, beta, gamma):
    for t in range(len(alpha)):
        for i in range(4):
            gamma[t][i] = alpha[t][i] + beta[t][i]
        s = log_sum(gamma[t])
        for i in range(4):
            gamma[t][i] -= s

    print("gamma end")
    
def calc_ksi(alpha, beta, A, B, o, ksi):
    T = len(alpha)
    temp = [0 for x in range(16)]
    for t in range(T-1):
        k = 0
        for i in range(4):
            for j in range(4):
                ksi[t][i][j] = alpha[t][i] + A[i][j] + B[j][ord(o[t+1])] + beta[t+1][j]
                temp[k] =ksi[t][i][j]
                k += 1
        s = log_sum(temp)
        for i in range(4):
            for j in range(4):
                ksi[t][i][j] -= s
    print("ksi end")

def bw(pi, A, B, alpha, beta, gamma, ksi, o):
    T = len(alpha)
    for i in range(4):
        pi[i] = gamma[0][i]
    s1 = [0 for x in range(T-1)]
    s2 = [0 for x in range(T-1)]
    for i in range(4):
        for j in range(4):
            for t in range(T-1):
                s1[t] = ksi[t][i][j]
                s2[t] = gamma[t][i]
            A[i][j] = log_sum(s1) - log_sum(s2)
    s1 = [0 for x in range(T)]
    s2 = [0 for x in range(T)]
    for i in range(4):
        for k in range(65536):
            if k % 10 == 0:
                print (i, k)
            valid = 0
            for t in range(T):
                if ord(o[t]) == k:
                    s1[valid] = gamma[t][i]
                    valid += 1
                s2[t] = gamma[t][i]
            if valid == 0:
                B[i][k] = -log_sum(s2)  # 平滑
            else:
                B[i][k] = log_sum(s1[:valid]) - log_sum(s2)


def baum_welch(pi, A, B):
    f = open("26.pku_training.utf8",'rb')
    sentence = f.read()[3:].decode('utf-8') # 跳过文件头
    f.close()
    T = len(sentence)   # 观测序列
    alpha = [[0 for i in range(4)] for t in range(T)]
    beta = [[0 for i in range(4)] for t in range(T)]
    gamma = [[0 for i in range(4)] for t in range(T)]
    ksi = [[[0 for j in range(4)] for i in range(4)] for t in range(T-1)]
    print("begain train")
    for time in range(100):
        print ("time:", time)
        calc_alpha(pi, A, B, sentence, alpha)    # alpha(t,i):给定lamda，在时刻t的状态为i且观测到o(1),o(2)...o(t)的概率
        calc_beta(pi, A, B, sentence, beta)      # beta(t,i)：给定lamda和时刻t的状态i，观测到o(t+1),o(t+2)...oT的概率
        calc_gamma(alpha, beta, gamma)           # gamma(t,i)：给定lamda和O，在时刻t状态位于i的概率
        calc_ksi(alpha, beta, A, B, sentence, ksi)    # ksi(t,i,j)：给定lamda和O，在时刻t状态位于i且在时刻i+1，状态位于j的概率
        bw(pi, A, B, alpha, beta, gamma, ksi, sentence) #baum_welch算法
        if (time>98):
            save_parameter(pi, A, B, time)


def list_write(f, v):
    for a in v:
        f.write(str(a))
        f.write(' ')
    f.write('\n')


def save_parameter(pi, A, B, time):
    f_pi = open("pi%d.txt" % time, "w")
    list_write(f_pi, pi)
    f_pi.close()
    f_A = open("A%d.txt" % time, "w")
    for a in A:
        list_write(f_A, a)
    f_A.close()
    f_B = open("B%d.txt" % time, "w")
    for b in B:
        list_write(f_B, b)
    f_B.close()


def train():
    # 初始化pi,A,B
    pi = [random.random() for x in range(4)]    # 初始分布
    log_normalize(pi)
    A = [[random.random() for y in range(4)] for x in range(4)] # 转移矩阵：B/M/E/S
    A[0][0] = A[0][3] = A[1][0] = A[1][3]\
        = A[2][1] = A[2][2] = A[3][1] = A[3][2] = 0 # 不可能事件
    B = [[random.random() for y in range(65536)] for x in range(4)]
    for i in range(4):
        log_normalize(A[i])
        log_normalize(B[i])
    print("into train")
    baum_welch(pi, A, B)
    return pi, A, B       
    
if __name__ == "__main__":
    
    pi, A, B = train()
#     f = open("26.mybook.txt",'rb')
#     data = f.read()[3:].decode('utf-8')
#     f.close()
    decode = viterbi(pi, A, B, '数据，前言思想')
    print(decode)
    segment('数据，前言思想', decode)

    