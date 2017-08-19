#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''
常量一直在图定义中，占用内存，
'''
a = tf.constant([3, 6])
b = tf.constant([2, 2])
c = tf.add(a, b) # >> [5 8]
d = tf.add_n([a, b, b]) # >> [7 10]. Equivalent to a + b + b
e = tf.mul(a, b) # >> [6 12] because mul is element wise
f = tf.matmul(a, b) # >> ValueError
g = tf.matmul(tf.reshape(a, [1, 2]), tf.reshape(b, [2, 1])) # >> [[18]]
h = tf.div(a, b) # >> [1 3]
i = tf.mod(a, b) # >> [1 0]

with tf.Session() as sess:
    x,y= sess.run([x,y])
    print (x)
    print (y)

'''
my_const = tf.constant([1.0, 2.0], name="my_const")
with tf.Session() as sess:
    print sess.graph.as_graph_def()
输出图的定义
'''
