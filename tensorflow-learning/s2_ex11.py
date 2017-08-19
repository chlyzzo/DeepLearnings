#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''
从给出的图结构，写出代码，

'''
a = tf.constant(2,name='a')
b = tf.constant(3,name='b')
x = tf.add(a,b,name='x')
y = tf.multiply(a,b,name='y')
useless = tf.multiply(a,x,name='useless')
z = tf.pow(y, x, name='z')
with tf.Session() as sess:
    writer = tf.summary.FileWriter('./graph1',sess.graph)
    z = sess.run(z)
    writer.close()


