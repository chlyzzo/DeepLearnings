#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''
变量，tensorflow中变量定义后，需要在session中执行初始化，可以全部一次性，单个或多个执行
Variable是一个类，而constant是一个操作，Variable的操作还有其他如下，
x.initializer # init op
x.value() # read op
x.assign(...) # write op
x.assign_add(...) # and more

全部变量一次性执行初始化
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    
执行初始化若干个
init_ab = tf.variables_initializer([a, b], name="init_ab")
with tf.Session() as sess:
    sess.run(init_ab)   
    
执行初始化单个
W = tf.Variable(tf.zeros([784,10]))
with tf.Session() as sess:
    sess.run(W.initializer) 
'''
# create variable a with scalar value
a = tf.Variable(2, name="scalar")
# create variable b as a vector
b = tf.Variable([2, 3], name="vector")
# create variable c as a 2x2 matrix
c = tf.Variable([[0, 1], [2, 3]], name="matrix")
# create variable W as 784 x 10 tensor, filled with zeros
w = tf.Variable(tf.truncated_normal([10,3]))

with tf.Session() as sess:
    sess.run(w.initializer)
    print(w.eval())# 不是print(w)

