#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''
tf.constant(value, dtype=None, shape=None,name='Const', verify_shape=False)

常量，需要在session中执行

tf.zeros(shape, dtype=tf.float32, name=None)
   tf.zeros([2, 3], tf.int32)
   
tf.zeros_like(input_tensor, dtype=None, name=None, optimize=True)
   把输入的tensor形状全部元素置成0，不改变原来的tensor形状类型

tf.ones(shape, dtype=tf.float32, name=None)
tf.ones_like(input_tensor, dtype=None, name=None, optimize=True)
同理于zeros

f.fill(dims, value, name=None)
   在dims的形状中填充单独的元素value，全部元素相同
   
tf.linspace(start, stop, num, name=None) 
     tf.linspace(10.0, 13.0, 4)
     
tf.range(start, limit=None, delta=1, dtype=None, name='range')
tf.range(start, limit, delta)
tf.range(limit)

随机值
tf.random_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None, name=None)
tf.truncated_normal(shape, mean=0.0, stddev=1.0, dtype=tf.float32, seed=None,name=None)
tf.random_uniform(shape, minval=0, maxval=None, dtype=tf.float32, seed=None,name=None)
tf.random_shuffle(value, seed=None, name=None)
tf.random_crop(value, size, seed=None, name=None)
tf.multinomial(logits, num_samples, seed=None, name=None)
tf.random_gamma(shape, alpha, beta=None, dtype=tf.float32, seed=None, name=None)

tf.set_random_seed(seed)

'''


a = tf.constant([2, 2], name="a")
b = tf.constant([[0, 1], [2, 3]], name="b")
x = tf.add(a, b, name="add")
y = tf.multiply(a, b, name="mul")

with tf.Session() as sess:
    x,y= sess.run([x,y])
    print (x)
    print (y)


