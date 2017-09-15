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
from pickletools import optimize
from numpy import gradient
import time


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
    
#把训练语料构成多个批次，每个批次是小的训练集，
def get_batches(int_text,batch_size,seq_length):
    """
    输入的很长的一个串，即长文本，但是其中词被替换成id，
    batch_size每个批次含记录的个数，即一个批次含多少个样本，
    seq_length，每个序列的长度，即一个样本的词长度，
    返回一个numpy数组，每个批次含记录,相当于一个list，x<-->y对应一个训练对，

    """
    words_per_batch = batch_size*seq_length #一个批次含词的个数，即一个批次的集合中含词的个数，
    print(len(int_text))
    print(words_per_batch)
    num_batches = len(int_text)//words_per_batch #一共有几个批次，
    print(num_batches)
    int_text = int_text[:num_batches*words_per_batch] #截取整数，即刚好满足批次数，
    y = np.array(int_text[1:]+[int_text[0]]) #把第一个词移到最后
    x = np.array(int_text)
    #这样x输入，y则是输出，保证词对应的输出是下一个词，训练有目标
    
    x_batches = np.split(x.reshape(batch_size,-1),num_batches,axis=1)
    #以水平切割x，x是行向量，x_batches则是切割后的数组，有多个，
    y_batches = np.split(y.reshape(batch_size,-1),num_batches,axis=1)
    
    batch_data = list(zip(x_batches,y_batches))
    return np.array(batch_data)

#开始训练

#获得全部书
book_filenames = sorted(glob.glob("myData/data/*.txt"))
print("found {} books".format(len(book_filenames)))

#获得书中的字符串，最后得到一个很长的串string，
corpus_raw = u""
for filename in book_filenames:
    with codecs.open(filename,'r','utf-8') as book_file:
        corpus_raw += book_file.read()
print("corpus is {} characters long.".format(len(corpus_raw)))

#语料处理，

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
pickle.dump((corpus_int,vocab_to_int,int_to_vocab,token_dict),open('./myData/train_ing_data/preprocess.p', 'wb'))

#设定超参数
num_epochs = 500
batch_size = 100
rnn_size = 100
num_layers = 3
keep_prob = 0.7
embed_dim = 512 
seq_length = 10
learning_rate = 0.001
save_dir = './myData/train_ing_data/save'

#建立神经网络图结构
train_graph = tf.Graph()
with train_graph.as_default():
    
    #初始化
    input_text = tf.placeholder(tf.int32, [None,None], name='input')
    targets = tf.placeholder(tf.int32,[None,None],name='targets')
    lr = tf.placeholder(tf.float32,name='learning_rate')
    
    #计算文本属性
    vocab_size = len(int_to_vocab)
    input_text_shape = tf.shape(input_text)
    
    #建立rnn神经单元
    lstm = tf.contrib.rnn.BasicLSTMCell(num_units=rnn_size)
    drop_cell = tf.contrib.rnn.DropoutWrapper(lstm,output_keep_prob=keep_prob)
    cell = tf.contrib.rnn.MultiRNNCell([drop_cell]*num_layers)
    
    #初始化状态
    initial_state = cell.zero_state(input_text_shape[0],tf.float32)
    initial_state = tf.identity(initial_state, name='initial_state')
    
    #创建词向量，输入近RNN
    embed = tf.contrib.layers.embed_sequence(input_text,vocab_size,embed_dim)
    
    #建立RNN
    outputs,final_state = tf.nn.dynamic_rnn(cell, embed, dtype=tf.float32)
    final_state = tf.identity(final_state, name='final_state')
    
    #输出计算loss
    logits = tf.contrib.layers.fully_connected(outputs, vocab_size, activation_fn=None)
    
    #计算生成每个词的概率
    props = tf.nn.softmax(logits, name='probs')
    
    #定义损失函数
    cost = tf.contrib.seq2seq.sequence_loss(
        logits,
        targets,
        tf.ones([input_text_shape[0],input_text_shape[1]])
        )
    
    #学习率优化
    optimizer = tf.train.AdamOptimizer(learning_rate)
    
    #避免梯度爆炸
    gradients = optimizer.compute_gradients(cost)
    capped_gradients = [(tf.clip_by_value(grad, -1.,1.),var) for grad, var in gradients if grad is not None]
    train_op = optimizer.apply_gradients(capped_gradients)
    
#训练
pickle.dump((seq_length,save_dir),open('./myData/train_ing_data/params.p','wb'))
batches = get_batches(corpus_int, batch_size, seq_length)
num_batches = len(batches)
print(num_batches)
start_time = time.time()

with tf.Session(graph=train_graph) as sess:
    sess.run(tf.global_variables_initializer())
    
    for epoch in range(num_epochs):
        state = sess.run(initial_state,{input_text:batches[0][0]})
        
        for batch_index,(x,y) in enumerate(batches):
            feed_dict = {
                input_text:x,
                targets:y,
                initial_state:state,
                lr:learning_rate
            }
            train_loss,state ,_=sess.run([cost,final_state,train_op],feed_dict) 
    
        time_elapsed = time.time()-start_time
        print('Epoch {:>3} Batch {:>4}/{}   train_loss = {:.3f}   time_elapsed = {:.3f}   time_remaining = {:.0f}'.format(
            epoch + 1,
            batch_index + 1,
            len(batches),
            train_loss,
            time_elapsed,
            ((num_batches * num_epochs)/((epoch + 1) * (batch_index + 1))) * time_elapsed - time_elapsed))   
        
        #每10次epochs保存模型
        if epoch % 10 ==0:
            saver =tf.train.Saver()
            saver.save(sess,save_dir)
            print('model trained and saved,')
            