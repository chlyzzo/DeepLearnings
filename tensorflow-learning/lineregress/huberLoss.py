#coding=utf-8

'''
Created on 20170820

@author: wenhaohu
'''

'''
huber loss
0.5*(y-f(x))^2
gama*|y-f(x)|-0.5*gama^2

'''
def huber_loss(labels,predictions,delta=1.0):
    residual = tf.abs(predictions-labels)
    condition = tf.less(residual,delta) #residual<delta??
    small_res = 0.5 * tf.square(residual)
    large_res = delta * residual-0.5 * tf.square(delta)
    return tf.select(condition,small_res,large_res)
