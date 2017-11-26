#coding=utf-8
'''
Created on 2017-11-2

@author: wenhaohu
'''

'''
卷积网络的例子
'''


import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data",one_hot=True)

sess = tf.InteractiveSession()

'''
初始化函数，因为卷积用到的初始化参数较多
'''
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=1)
    return tf.Variable(initial)
def bias_variable(shape):
    initial = tf.constant(0.1,shape=shape)
    return tf.Variable(initial)

'''
2维的卷积，
x输入的图像，一般是[None,图像展开维数]，第一个值是样本量，可不给具体值
w参数，[卷积核，channel=图像灰度，卷积核数量]
strdes卷积核移动的方式，
'''
def conv2d(x,W):
   return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
'''
最大池化
2x2--->1x1
'''
def max_pool_2x2(x):
   return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
'''
设计输入输出,注意的是，卷积操作是图像28*28，需要把一维的转成2d图像，reshape，
'''
x = tf.placeholder(tf.float32, [None,784])
y_ = tf.placeholder(tf.float32,[None,10])
x_image = tf.reshape(x, [-1,28,28,1])

'''
28x28-->14*14*32
'''
W_conv1 = weight_variable([5,5,1,32])
b_conv1 = bias_variable([32])#一个卷积核一个偏置，共享参数
h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)#第一个卷积层后激活函数
h_pool1 = max_pool_2x2(h_conv1)#卷积层后，再激活函数后，进行池化

'''
14x14x32---->7x7x64
'''
W_conv2 = weight_variable([5,5,32,64])#第一卷积层后有32个featuresMap
b_conv2 = bias_variable([64])#一个卷积核一个偏置，共享参数
h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)#第一个卷积层后激活函数
h_pool2 = max_pool_2x2(h_conv2)#卷积层后，再激活函数后，进行池化

'''
7x7x64--->7*7*64X1024，
卷积后再进行全连接，最后得到输出
'''
W_fc1 = weight_variable(7*7*64,1024)
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])#展开成一维
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)

'''
全连接后dropout
'''
keep_prop = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prop)

'''
连接softmax
'''
W_fc2 = weight_variable([1024,10])
b_fc2 = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)

'''
定义评价
'''

cross_entropy = tf.reduce_mean( -tf.reduce_sum( y_*tf.log(y_conv),reduction_indices=[1] ) )
train_step = tf.train.AdagradOptimizer(1e-4).minimize(cross_entropy)

#结果评测
correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
accuracy =  tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

#开始训练
tf.global_variables_initializer().runn()
for i in range(20000):
  batch = mnist.train.next_batch(50) #每个批次选取50个样本
  if i%100==0:
    train_accuracy = accuracy.eval(
          feed_dict={x:batch[0],y_:batch[1],keep_prop:1.0}
        )
    print("step %d ,trainning accuracy %g" %(i,train_accuracy)) 
  train_step.run(feed_dict={x:batch[0],y_:batch[1],keep_prop:0.5})

'''
测试集的效果
'''
print("test accuracy %g"%accuracy.eval(feed_dict={
    x:mnist.test.imags,y_:mnist.test.labels,keep_prop:1.0
    }))
    
    
    
    
    
