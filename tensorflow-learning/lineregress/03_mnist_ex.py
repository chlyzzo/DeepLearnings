#coding=utf-8

'''
Created on 20170820

@author: wenhaohu
'''
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.training import learning_rate_decay
from tensorflow.contrib.factorization.examples.mnist import fill_feed_dict
import time

#step1，读取数据源，
MNIST = input_data.read_data_sets('E:/workspace/DeepLearnings/tensorflow-learning/data/mnist',one_hot=True)
#tensorflow.contrib.learn.python.learn.datasets.base.Datasets
#MNIST.train.num_examples 查样本数量，

#step2，设置参数
learning_rate = 0.01
batch_size = 128
n_epochs = 25

#step3 设置placholder，存储样本和标签
X = tf.placeholder(tf.float32,[batch_size,784])
Y = tf.placeholder(tf.float32,[batch_size,10])

#step4,设置训练参数，权重w和偏置bias
#并且初始值，使用概率分布

w = tf.Variable(tf.random_normal(shape=[784,10],stddev=0.01), name='weights')
b = tf.Variable(tf.zeros(shape=[1,10]), name='bias')
                
#step5,预测
logits = tf.matmul(X,w) + b

#step6，定义损失函数
#多类别输出，softmax，采取交叉熵，
entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=Y)
loss = tf.reduce_mean(entropy)

#step7，设置训练操作
#即优化方法，批处理，
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)

#变量参数初始化
init = tf.global_variables_initializer()

with tf.Session() as sess:
    writer = tf.summary.FileWriter('./graphs/logistic_reg', sess.graph)
    sess.run(init) #变量初始化
    start_time = time.time()    
    
    n_batches = int (MNIST.train.num_examples/batch_size)
    for i in range(n_epochs):
        total_loss = 0
        for _ in range(n_batches):
            X_batch,Y_batch = MNIST.train.next_batch(batch_size)
            _,loss_batch = sess.run([optimizer,loss],feed_dict={X:X_batch,Y:Y_batch})
            total_loss += loss_batch
        print('Average loss epoch {0}: {1}'.format(i, total_loss/n_batches))
    print('Total time: {0} seconds'.format(time.time() - start_time))            
    print('Optimization Finished!')         
            
    #测试模型

    n_batches = int(MNIST.test.num_examples/batch_size)
    
    total_correct_preds = 0
    
    for i in range(n_batches):
        X_batch, Y_batch = MNIST.test.next_batch(batch_size)
        _,loss_batch,logits_batch = sess.run([optimizer,loss,logits], feed_dict={X: X_batch, Y:Y_batch})
        preds = tf.nn.softmax(logits_batch)
        correct_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(Y_batch, 1))
        accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32))
        total_correct_preds += sess.run(accuracy)
        
    print('Accuracy {0}'.format(total_correct_preds/MNIST.test.num_examples))
    writer.close()
    