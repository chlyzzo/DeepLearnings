#coding=utf-8
'''
Created on 2017-09-04

@author: wenhaohu
'''
import numpy as np
import tensorflow as tf
import glob
import codecs
import pickle


#获得全部书
book_filenames = sorted(glob.glob("data/*.txt"))
print("found {} books".format(len(book_filenames)))

#获得书中的字符串，最后得到一个很长的串string，
corpus_raw = u""
for filename in book_filenames:
    with codecs.open(filename,'r','utf-8') as book_file:
        corpus_raw += book_file.read()
print("corpus is {} characters long.".format(len(corpus_raw)))

#语料处理，

def create_lookup_tables(text):
    """
    创建单词的字典，即词与id，id与词的对应关系
    需要对文本进行split
    返回两个字典(vocab_to_int,int_to_cocab)
    """
    vocab = set(text)
    int_to_vocab = {key:word for key,word in enumerate(vocab)}
    vocab_to_int = {word:key for key,word in enumerate(vocab)}
    return vocab_to_int,int_to_vocab
#切割标点符号

def token_lookup():
    """
    标点符号的字典，
    """
    return {
        '.': '||period||',
        ',': '||comma||',
        '"': '||quotes||',
        ';': '||semicolon||',
        '!': '||exclamation-mark||',
        '?': '||question-mark||',
        '(': '||left-parentheses||',
        ')': '||right-parentheses||',
        '--': '||emm-dash||',
        '\n': '||return||'
        }
    
#预处理并保存数据
token_dict = token_lookup()#标点符号
for token,replacement in token_dict.items():
    corpus_raw = corpus_raw.replace(token, '{}'.format(replacement))
#标点符号替代掉，变成小写，切割出单词
corpus_raw = corpus_raw.lower()
corpus_raw = corpus_raw.split()
#得到词与id的对应关系
vocab_to_int,int_to_vocab = create_lookup_tables(corpus_raw)
corpus_int = [vocab_to_int[word] for word in corpus_raw]
pickle.dump((corpus_int,vocab_to_int,int_to_vocab,token_dict),open('preprocess.p', 'wb'))


#把训练语料构成多个批次，每个批次是小的训练集，
def get_batches(int_text,batch_size,seq_length):
    """
    输入的很长的一个串，即长文本，但是其中词被替换成id，
    batch_size每个批次含记录的个数，即一个批次含多少个样本，
    seq_length，每个序列的长度，即一个样本的词长度，
    返回一个numpy数组，每个批次含记录,相当于一个list，x<-->y对应一个训练对，

    """
    words_per_batch = batch_size*seq_length #一个批次含词的个数，即一个批次的集合中含词的个数，
    num_batches = len(int_text)//words_per_batch #一共有几个批次，
    int_text = int_text[:num_batches*words_per_batch] #截取整数，即刚好满足批次数，
    
    y = np.array(int_text[1:]+[int_text[0]]) #把第一个词移到最后
    x = np.array(int_text)
    #这样x输入，y则是输出，保证词对应的输出是下一个词，训练有目标
    
    x_batches = np.split(x.reshape(batch_size,-1),num_batches,axis=1)
    #以水平切割x，x是行向量，x_batches则是切割后的数组，有多个，
    y_batches = np.split(y.reshape(batch_size,-1),num_batches,axis=1)
    
    batch_data = list(zip(x_batches,y_batches))
    return np.array(batch_data)


#设定超参数
num_epochs = 10000
batch_size = 512
rnn_size = 512
num_layers = 3
keep_prob = 0.7
embed_dim = 512 
seq_length = 30
learning_rate = 0.001
save_dir = './save'



    
    
    
    
    
    
