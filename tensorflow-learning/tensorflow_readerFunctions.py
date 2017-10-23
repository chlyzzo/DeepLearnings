#coding=utf-8

'''
Created on 2017-10-12

@author: wenhaohu
'''
'''
喂入数据的几个问题：

喂入数据的流程，存储-->客户端--->worker,当客户端和worker在不同机器时，很慢，

所以，把数据放到worker中，是很快的，比如Python’s generator

在tensorflow中的读取数据函数：

1，tf.TextLineReader
   Outputs the lines of a file delimited by newlines
   E.g. text files, CSV files
   
2，   tf.FixedLengthRecordReader
   Outputs the entire file when all files have same fixed lengths
   E.g. each MNIST file has 28 x 28 pixels, CIFAR-10 32 x 32 x 3
   
3，tf.WholeFileReader
    Outputs the entire file content   
    
4，tf.TFRecordReader
    Reads samples from TensorFlow’s own binary format (TFRecord)  
    
5，tf.ReaderBase
    To allow you to create your own readers 
         
'''

import tensorflow as tf

filename_queue = tf.train.string_input_producer(["data/file0.csv", "data/file1.csv"],num_epochs=1)
reader = tf.TextLineReader()
key, value = reader.read(filename_queue)

with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    tf.train.start_queue_runners()
    num_examples = 0
    try:
        while True:
                s_key, s_value = sess.run([key, value])
                print( s_key, s_value)
        num_examples += 1
    except tf.errors.OutOfRangeError:
            print ("There are", num_examples, "examples")


