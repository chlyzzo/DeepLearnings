#coding=utf-8

'''
Created on 2017年10月12日

@author: wenhaohu
'''

'''
使用tensorflow计算函数的偏导数，并计算值
tf.gradients(y,[xs])
y是[xs]变量的函数，
该函数分别计算给定变量的偏导数的值，当变量都给定值
'''
import tensorflow as tf

x = tf.Variable(2.0)
y = 2.0 * (x**3)
z= 3.0 + y**2

grad_z = tf.gradients(z,[x,y])

with tf.Session() as sess:
    sess.run(x.initializer)
    print(sess.run(grad_z)) # [768.0, 32.0]


'''
梯度（变量的偏导数的累加），出现的问题：
1，梯度消失


2，梯度爆炸



'''
