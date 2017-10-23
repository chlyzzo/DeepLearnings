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



