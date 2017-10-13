#coding=utf-8

'''
Created on 2017-10-12

@author: wenhaohu
'''

'''
tensorflow的保存，把训练过程进行保存，

tf.train.Saver.save(sess, save_path,global_step=None...)

保存session不是graph，

'''

'''
global step，有何用呢？

self.global_step = tf.Variable(0, dtype=tf.int32, trainable=False,name='global_step')
self.optimizer = tf.train.GradientDescentOptimizer(self.lr).minimize(self.loss,global_step=self.global_step)

初始化0，会随着优化变化而自增，
'''


'''
Visualize our summary statistics during our training
tf.summary.scalar
tf.summary.histogram
tf.summary.image

summary，保存参数变化，可以在
设置：
with tf.name_scope("summaries"):
   tf.summary.scalar("loss", self.loss
   tf.summary.scalar("accuracy", self.accuracy)
   tf.summary.histogram("histogram loss", self.loss)
   # merge them all
   self.summary_op = tf.summary.merge_all()

运行：
loss_batch, _, summary = sess.run([model.loss, model.optimizer,
model.summary_op],
feed_dict=feed_dict)

保存：
writer.add_summary(summary, global_step=step)

查看：
在TensorBoard中查看，
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

