#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''

feed_dict任意可改变值的tensor，

'''
a = tf.add(2,5)
b = tf.multiply(a,3)

with tf.Session() as sess:
    replace_dict = {a:15}
    print(sess.run(b,feed_dict=replace_dict))#45
    
