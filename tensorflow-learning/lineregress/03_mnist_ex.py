#coding=utf-8

'''
Created on 20170820

@author: wenhaohu
'''
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
MNIST = input_data.read_data_sets('E:/workspace/DeepLearnings/tensorflow-learning/data/mnist',one_hot=True)
#tensorflow.contrib.learn.python.learn.datasets.base.Datasets
#MNIST.train.num_examples 查样本数量，

print(MNIST.train.num_examples)
print(MNIST.validation.num_examples)
print(MNIST.test.num_examples)

X = tf.placeholder(tf.float32, [batch_size,784], name='image')
Y = tf.placeholder(tf.float32,[batch_size,10],name='label')







