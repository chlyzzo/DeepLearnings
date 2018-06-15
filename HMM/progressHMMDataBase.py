#coding=utf-8
'''
Created on 2018-06-13

@author: wenhaohu

统计形式得到pi,A,B三个参数
'''
import math
import numpy as np

infinite = float(-2**31)

'''
a[i]=log(a[i])-log(sum(a[]))
'''
def log_normalize(a):
    s = 0
    for x in a:
        s += x
    if s == 0:
        print ("Error..from log_normalize.")
        return
    s = math.log(s)
    for i in range(len(a)):
        if a[i] == 0:
            a[i] = infinite
        else:
            a[i] = math.log(a[i]) - s

'''
从训练集中统计状态转移矩阵，发射矩阵，状态先验值
'''            
def mle():  # 0B/1M/2E/3S
    pi = [0] * 4   # 列向量pi一维向量，代表状态的个数,pi[0]=第一个状态
    a = [[0] * 4 for x in range(4)] # 4*4,状态转移矩阵，即一个状态到另一个状态的个数，
    b = [[0]* 65536 for x in range(4)]  # 4*65536,状态到字符的个数
    # 以二进制流读取，将编码统一
    f = open(r"26.pku_training.utf8","rb")
    '''
           文件读取前面有不必要的字符存在，所以从第三3个字符开始读取；
           有的是6开始截取
           另外需要替换掉换行符
    '''
    data = f.read()[3:].decode('utf-8').replace('\r\n','')
    f.close()
    tokens = data.split('  ')
    # 增加英文词训练集
    f = open(r'26.Englishword.train','rb')
    data = f.read().decode('utf-8').replace('\r\n','')
    f.close()
    tokens.extend(data.split(' '))
    '''
    tokens是分词后的单词item集合，18115156个item
    '''
    #开始训练
    last_q = 2
    old_progress = 0
    print('进度')
    for k,token in enumerate(tokens):
        progress = float(k)/float(len(tokens))
        if progress > old_progress + 0.1:
            print('%.3f%%' % (progress * 100))
            old_progress = progress
        token = token.strip() #去除空格等，中间的去不掉
        n = len(token)
        if n<=0: #非字符
            continue
        if n==1: #单字
            pi[3] += 1 #长度1的字符,即单字，字对应的状态是结尾，状态是3
            a[last_q][3] += 1 #状态转移矩阵，转到结束词的状态链，-->S
            b[3][ord(token[0])] += 1 # 字符是单字个数，ord是单个字符的ascii编码，
            last_q= 3
            continue
        # 初始向量，长度大于等于2的词，状态次数先加起来
        pi[0] +=1 #词开始
        pi[2] +=1 #词结束
        pi[1] +=(n-2) #词中间，即去掉首尾词，剩下的是中间的出现次数
        '''
                    计算状态间转移次数，状态转移矩阵，
                   注意词长度不同，状态也不同
        '''
        a[last_q][0] +=1 #上一个状态到词开始，上一个状态是词结束2或词单字3
        last_q=2
        if n ==2 :
            a[0][2] +=1 #词长度=2，词开始到词结束状态+1，
        else:           #词长度大于2
            a[0][1] +=1 #词开始到词结束状态+1，
            a[1][1] +=(n-3) # 词中间到词中间状态+(n-3)，因为三个词中间词无状态转移，4个词就一次转移
            a[1][2] +=1 #词开始到词结束状态+1
        '''
                  发射矩阵，4*65535，状态到词的次数
        '''
        b[0][ord(token[0])] +=1 #词开始状态与该字符次数加1
        b[2][ord(token[n-1])] +=1 #词结束状态与该字符次数加1
        for i in range(1,n-1): #多个中间字符处于词中间
            b[1][ord(token[i])] +=1 #词中间状态到该字符的次数加1
    #正则化
    log_normalize(pi)
    for i in range(4):
        log_normalize(a[i])
        log_normalize(b[i])
    return [pi,a,b]

'''
写入文件，一个数组写入到文件中
'''
def list_write(f, v):
    for a in v:
        f.write(str(a))
        f.write(' ')
    f.write('\n')

'''
保存参数
'''    
def save_parameter(pi, A, B):
    f_pi = open("pi.txt", "w")
    list_write(f_pi, pi) #pi只有4*1
    f_pi.close()
    f_A = open("A.txt", "w")
    for a in A:
        list_write(f_A, a) #a 是4*4
    f_A.close()
    f_B = open("B.txt", "w")
    for b in B:
        list_write(f_B, b) # b是4*65535
    f_B.close()
    
if __name__ == "__main__":
#     pi,A,B=mle()
#     save_parameter(pi, A, B)
    tr = np.linspace(0, 0.8, 5)
    print(tr)


