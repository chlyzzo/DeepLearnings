#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

W = tf.Variable(10)
W.assign(100) #这是一个操作，没有在session中执行将不会起到作用
with tf.Session() as sess:
   sess.run(W.initializer)
   print(W.eval()) # >> 10
   
'''
assign需要操作在session中执行
W = tf.Variable(10)
assign_op = W.assign(100)
with tf.Session() as sess:
   sess.run(W.initializer)
   sess.run(assign_op)
   print W.eval() # >> 100

但是，这样子就不用执行初始化了，   assign_op已经做了
W = tf.Variable(10)
assign_op = W.assign(100)
with tf.Session() as sess:
   sess.run(assign_op)
   print W.eval() # >> 100   
   
初始化其实就是经op操作，把值赋给变量本身
'''