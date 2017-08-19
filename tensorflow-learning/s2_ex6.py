#coding=utf-8

'''
Created on 2017-08-19

@author: wenhaohu
'''
import tensorflow as tf

# create a variable whose original value is 2
my_var = tf.Variable(2, name="my_var")
# assign a * 2 to a and call that op a_times_two
my_var_times_two = my_var.assign(2 * my_var) #把 2 * my_var写进my_var里
with tf.Session() as sess:
   sess.run(my_var.initializer)
   print(sess.run(my_var_times_two)) # >> 4
   print(sess.run(my_var_times_two)) # >> 8
   print(sess.run(my_var_times_two)) # >> 16   


'''
同理assign_add()和assign_sub()，把数值进行加减赋给变量
这两个需要初始值，

my_var = tf.Variable(10)
With tf.Session() as sess:
sess.run(my_var.initializer)
    # increment by 10
    sess.run(my_var.assign_add(10)) # >> 20
    # decrement by 2
    sess.run(my_var.assign_sub(2)) # >> 18

不同session里的变量是隔离的，尽管名字相同，值还是不同的。

'''


