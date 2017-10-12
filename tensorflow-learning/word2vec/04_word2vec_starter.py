#coding=utf-8

""" The mo frills implementation of word2vec skip-gram model using NCE loss. 
Author: Chip Huyen
Prepared for the class CS 20SI: "TensorFlow for Deep Learning Research"
cs20si.stanford.edu
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector

from process_data import process_data

VOCAB_SIZE = 500 #词典大小
BATCH_SIZE = 128 # 每个批次的大小，即每个批次包含的样本量
EMBED_SIZE = 20 # 每个词的嵌入向量大小，即词向量维度
SKIP_WINDOW = 1 # 窗口，即中心词调几个词
NUM_SAMPLED = 64    # 抽样时取的负样本个数
LEARNING_RATE = 1.0
NUM_TRAIN_STEPS = 200
SKIP_STEP = 50 # 优化loss，训练多少次

def outputEmbed(weigths):
    cnt = 1
    for row in weigths:
        if cnt>5:
            break
        print(row)
        cnt = cnt + 1

def word2vec(batch_gen):
    """ Build the graph for word2vec model and train it """
    # 使用placeholders设置输入和输出，即中心词和目标词
    with tf.name_scope('data'):
        center_words = tf.placeholder(tf.int32, shape=[BATCH_SIZE], name='center_words')
        target_words = tf.placeholder(tf.int32,shape=[BATCH_SIZE,1],name='target_words')

    # 词嵌入矩阵[词典大小,词向量大小]
    with tf.name_scope('mbedding_matrix'):
        embed_matrix = tf.Variable(tf.random_uniform([VOCAB_SIZE, EMBED_SIZE], -1.0, 1.0), name='embed_matrix')
    
    # 模型
    # tf.nn.embedding_lookup，根据input_ids中的id，寻找embedding中的对应向量（一行，从0开始计数）然后组成新的矩阵，
    # embed = tf.nn.embedding_lookup(embed_matrix, center_words, name='embed')
    # 开始训练，设置w和b，
    with tf.name_scope('loss'):
        embed = tf.nn.embedding_lookup(embed_matrix,center_words,name='embed')
        # Step 4: construct variables for NCE loss
        nce_weight = tf.Variable(tf.truncated_normal([VOCAB_SIZE, EMBED_SIZE],stddev=1.0 / (EMBED_SIZE ** 0.5)), name='nce_weight')
        nce_bias = tf.Variable(tf.zeros([VOCAB_SIZE]), name='nce_bias')
        # nce损失函数
        loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weight, 
                                            biases=nce_bias,
                                            labels=target_words,
                                            inputs=embed,
                                            num_sampled=NUM_SAMPLED,#负样本数
                                            num_classes=VOCAB_SIZE), name='loss')

        
    # 优化
    optimizer = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(loss)

    #迭代训练
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        
        #输出初始化的词嵌入矩阵
        outputEmbed(embed_matrix.eval())
        
        total_loss = 0.0 #总的loss
        writer = tf.summary.FileWriter('w2v_exter_files/.my_graph/no_frills/', sess.graph)
        for index in range(NUM_TRAIN_STEPS):
            centers, targets = next(batch_gen)
            loss_batch,_ = sess.run([loss,optimizer],feed_dict={center_words:centers,target_words:targets})

            total_loss += loss_batch
            if (index + 1) % SKIP_STEP == 0:
                print('Average loss at step {}: {:5.1f}'.format(index, total_loss / SKIP_STEP))
                total_loss = 0.0
        writer.close()
        #最后训练完，把词向量保存，是embed_matrix;embed_matrix.eval()是numpy.ndarray
        outputEmbed(embed_matrix.eval())
        #outputEmbed(nce_weight.eval())

def main():
    batch_gen = process_data(VOCAB_SIZE, BATCH_SIZE, SKIP_WINDOW)
    word2vec(batch_gen)

if __name__ == '__main__':
    main()
