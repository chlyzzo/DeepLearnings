#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

'''
一个变量来初始化另一个变量
W = tf.Variable(tf.truncated_normal([700, 10]))
U = tf.Variable(2 * W)

这种方式不是安全的，因为变量W未初始化，

更加安全的方式如下：
U = tf.Variable(2 * W.intialized_value())
确保w的变量初始化先于U变量的初始化。


'''

'''
session 和 InteractiveSession

InteractiveSession本身默认（？）
即不需要再session里run，而会自动执行。

sess = tf.InteractiveSession()
a = tf.constant(5.0)
b = tf.constant(6.0)
c = a * b
# We can just use 'c.eval()' without specifying the context 'sess'
print(c.eval())
sess.close()
'''

sess = tf.InteractiveSession()
a = tf.constant(5.0)
b = tf.constant(6.0)
c = a * b
# We can just use 'c.eval()' without specifying the context 'sess'
print(c.eval())
sess.close()

'''
控制依赖，即控制变量的运行顺序，
d,e操作在abc操作之后执行

with g.control_dependencies([a, b, c]):
   # 'd' and 'e' will only run after 'a', 'b', and 'c' have executed.
   d = ...
   e = …

'''



