#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''
lazy loading

'''

'''
正常的形式

x = tf.Variable(10,name='x')
y = tf.Variable(20,name='y')
z = tf.add(x,y)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter('./my_graph/12',sess.graph)
    for _ in range(10):
        print(sess.run(z))
    writer.close()
'''   
 
'''
lazy加载形式
查看图时，会看不到add节点，不是bug，是真的看不到

tf.get_default_graph().as_graph_def()
可以看到有add操作，出现多次；而在正常下只有一次；

'''
x = tf.Variable(10,name='x')
y = tf.Variable(20,name='y')
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter('./my_graph/12',sess.graph)
    for _ in range(10):
        print(sess.run(tf.add(x,y)))
    writer.close()

