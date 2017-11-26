#coding=utf-8
'''
Created on 2017-11-23

@author: wenhaohu

实现进阶的卷积网络，
'''
'''
使用cifar10读取数据集
'''

import cifar10,cifar10_input
import tensorflow as tf
import numpy as np
import time
from pip._vendor.appdirs import site_data_dir
from tensorflow.contrib.layers.python.layers.layers import bias_add
from numpy import shape
from tensorflow.contrib.nn.python.ops import cross_entropy
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

'''
设置批大小，轮数，下载数据的路径
'''
max_steps = 3000
batch_size = 128
data_dir = '/tmp/cifar10_data/cifar-10-batches-bin'

'''
权重设置，
正则化，L2正则，特征权重也算一部分损失，
L1正则会造成稀疏特征，大部分无用特征被置为0，L2正则让特征不过大，变得平均，
wl控制l2 loss的大小，nn.l2_loss计算l2 loss，
'''

def variable_with_weight_loss(shape,stddev,wl):
    var = tf.Variable(tf.truncated_normal(shape, stddev=stddev))
    if wl is not None:
        weight_loss = tf.multiply(tf.nn.l2_loss(var), wl, name='weight_loss')
        tf.add_to_collection('losses',weight_loss)
    return var

'''
distorted_inputs函数，对数据增强操作，含如下操作：
随机水平翻转，随机剪切24*24大小图片，随机亮度和对比度，数据标准化
扩大样本量，16个独立线程加速，

inputs，生成测试集，不需要对数据增强，只需读取源数据即可，
'''
cifar10.maybe_download_and_extract()

images_train,labels_train = cifar10_input.distorted_inputs(data_dir=site_data_dir,batch_size=batch_size)

images_test,labels_test = cifar10_input.inputs(eval_data=True,data_dir=data_dir,batch_size=batch_size)

'''
输入的placeholder，特征和label的
数据尺寸固定下来[batch_size,24,24,3]
裁剪后是24*24,3是三色道，rgb，
'''
image_holder = tf.placeholder(tf.float32, [batch_size,24,24,3])
label_holder = tf.placeholder(tf.int32,[batch_size])

'''
第一层卷积，
设置权重，卷积核5*5,3色道，64个卷积核，不对第一层weight进行l2正则，wl=0.0，

conv2d对image_holder卷积，步长均1，模式same；bias为0；使用relu激活；
卷积后，用3*3，步长2*2最大池化，
再用lrn处理，响应大的相对更大，抑制反馈小的神经元，增强泛化能力，lrn对relu无上界的激活函数有用，不适合sigmoid有边界的。

'''
weight1 = variable_with_weight_loss(shape=[5,5,3,64], stddev=5e-2, wl=0.0)
kernel1 = tf.nn.conv2d(image_holder,weight1,[1,1,1,1],padding='SAME')
bias1 = tf.Variable(tf.constant(0.0,shape=[64]))
conv1 = tf.nn.relu(tf.nn.bias_add(kernel1,bias1))
pool1 = tf.nn.max_pool(conv1,ksize=[1,3,3,1],strides=[1,2,2,1],padding='SAME')
norm1 = tf.nn.lrn(pool1,4,bias=1.0,alpha=0.001/9.0,beta=0.75)

'''
第二层
上一层64个卷积核，输出有64个通道；
然后偏置设置0.1（为什么呢？）
先进行lrn再最大池化，

'''
weight2 = variable_with_weight_loss(shape=[5,5,3,64], stddev=5e-2, wl=0.0)
kernel2 = tf.nn.conv2d(norm1,weight2,[1,1,1,1],padding='SAME')
bias2 = tf.Variable(tf.constant(0.1,shape=[64]))
conv2 = tf.nn.relu(tf.nn.bias_add(kernel2,bias2))
norm2 = tf.nn.lrn(conv2,4,bias=1.0,alpha=0.001/9.0,beta=0.75)
pool2 = tf.nn.max_pool(norm2,ksize=[1,3,3,1],strides=[1,2,2,1],padding='SAME')

'''
第三层，全连接层
需要要把第二层的输出flatten，
tf.reshape把每个样本变成一维向量，get_shape=扁平化后的长度，
全连接层不过拟合，使用l2正则，wl=0.04，relu激活；

'''
reshape = tf.reshape(pool2, [batch_size,-1])
dim = reshape.get_shape()[1].value
weight3 = variable_with_weight_loss(shape=[dim,384], stddev=0.04, wl=0.004)
bias3 = tf.Variable(tf.constant(0.1,shape=[384]))
local3 = tf.nn.relu(tf.matmul(reshape, weight3)+bias3)

'''
第4层，与全连接层类似，只是节点降到一半，
其他参数不变

'''
weight4 = variable_with_weight_loss(shape=[384,192], stddev=0.04, wl=0.04)
bias4 = tf.Variable(tf.constant(0.1,shape=[192]))
local4 = tf.nn.relu(tf.matmul(local3,weight4)+bias4)

'''
第5层，输出层
output=x*w+bias

'''
weight5 = variable_with_weight_loss(shape=[192,10], stddev=1/192.0, wl=0.0)
bias5 = tf.variable(tf.constant(0.0,shape=[10]))
logits = tf.add(tf.matmul(local4,weight5),bias5)

'''
网络的结构如下：
conv1 卷积层和relu激活
pool1 最大池化
norm1 LRN
conv2 卷积层和relu激活
norm2 lrn
pool2 最大池化
local3 全连接和relu激活
local4 全连接和relu激活
logits 模型inference输出结果

'''


def loss(logits,labels):
    labels = tf.cast(labels,tf.int64)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits=logits,labels=labels,name='cross_entropy_per_example'
        )
    
    cross_entropy_mean = tf.reduce_mean(cross_entropy,name='cross_entropy')
    tf.add_to_collection('losses', cross_entropy_mean)
    return tf.add_n(tf.get_collection('losses'), name='total_loss')

loss = loss(logits,label_holder)

train_op = tf.train.AdagradDAOptimizer(1e-3).minimize(loss)

top_k_op = tf.nn.in_top_k(logits, label_holder, 1)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

tf.train.start_queue_runners()

'''
开始训练
'''
for step in range(max_steps):
    start_time = time.time()
    image_batch.label_batch = sess.run([image_train,label_train])
    _,loss_value = sess.run([train_op,loss],feed_dict=
                            {image_holder:image_holder,label_holder:label_batch}
                            )
    duration = time.time()-start_time
    if step % 10 ==0:
        example_per_sec = batch_size / duration
        sec_per_batch = float(duration)
        
        format_str = ('step %d,loss=%.2f (%.1f example/sec;%.3f sec/batch)')
        print(format_str % (step,loss_value,example_per_sec,sec_per_batch))
      

'''
预测
'''
num_examples = 10000
import math
num_iter = int(math.ceil(num_examples / batch_size))
true_count = 0
total_sample_count = num_iter * batch_size
step = 0
while step<num_iter:
    image_batch,label_batch = sess.run([image_test,label_test])
    predictions = sess.run([top_k_op],feed_dict={image_holder:image_batch,
                                                  label_holder:label_batch
        })
    true_count += np.sum(predictions)
    step += 1
  
precision = true_count /total_sample_count
print('precision @ 1= %.3f' % precision)  





