#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''
placeholders

tf.placehoders(dtype,shape=None,name=None)

如果使用tf.placehoders后，必须feed值，不然出错。

shape可以None，即接收任何形状的数据，根据给定数据形式确定形状，
placehoders可以认为是一个操作，

feed多个数据，使用for
with tf.Session() as sess:
   for a_value in list_of_values_for_a:
       print sess.run(c, {a: a_value})


tf.Graph.is_feedable(tensor)
判断一个tensor是否可以feed数据进去，是则返回true。

'''
a = tf.placeholder(tf.float32,shape=[3])
b = tf.constant([5,5,5],tf.float32)
c = a+5

with tf.Session() as sess:
    #print(sess.run(c)) #error 因为a没有任何值，需要feed值进去
    print (sess.run(c,{a:[1,2,3]})) #a是tensor的key，不是字符串a，


