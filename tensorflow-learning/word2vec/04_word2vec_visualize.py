#coding=utf-8

""" 
word2vec with NCE loss and code to visualize the embeddings on TensorBoard
Author: Chip Huyen
Prepared for the class CS 20SI: "TensorFlow for Deep Learning Research"
cs20si.stanford.edu
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
from tensorflow.contrib.tensorboard.plugins import projector
import tensorflow as tf

from process_data import process_data
import utils

VOCAB_SIZE = 50000
BATCH_SIZE = 128
EMBED_SIZE = 128 # dimension of the word embedding vectors
SKIP_WINDOW = 1 # the context window
NUM_SAMPLED = 64    # Number of negative examples to sample.
LEARNING_RATE = 1.0
NUM_TRAIN_STEPS = 100000
WEIGHTS_FLD = 'w2v_exter_files/processed/'
SKIP_STEP = 2000

class SkipGramModel:
    """ 
    构建一个图，用于word2vec模型
    拥有的变量：
    vocab_size，词典大小
    embed_size，词向量大小
    batch_size，批次的样本数量
    num_sampled，负样本的数量
    lr，学习率
    global_step，迭代多少步输出loss
    """
    def __init__(self, vocab_size, embed_size, batch_size, num_sampled, learning_rate):
        self.vocab_size = vocab_size
        self.embed_size = embed_size
        self.batch_size = batch_size
        self.num_sampled = num_sampled
        self.lr = learning_rate
        self.global_step = tf.Variable(0, dtype=tf.int32, trainable=False, name='global_step')

    def _create_placeholders(self):
        """  
                         定义模型的输入和输出，使用placeholders，
        """
        with tf.name_scope("data"):
            self.center_words = tf.placeholder(tf.int32, shape=[self.batch_size], name='center_words')
            self.target_words = tf.placeholder(tf.int32, shape=[self.batch_size, 1], name='target_words')

    def _create_embedding(self):
        """ 
                    定义权重，需要训练的，也是最后的结果，我们所关心的就是该权重值，
                   需要初始化权重，权重的shape是[词典大小，词向量大小]
        """
        # 默认cpu，当然有gpu只需更改
        with tf.device('/cpu:0'):
            with tf.name_scope("embed"):
                self.embed_matrix = tf.Variable(tf.random_uniform([self.vocab_size, 
                                                                    self.embed_size], -1.0, 1.0), 
                                                                    name='embed_matrix')

    def _create_loss(self):
        """ 
        设定模型，关键是损失函数的定义
        """
        with tf.device('/cpu:0'):
            with tf.name_scope("loss"):
                # Step 3: 样本
                embed = tf.nn.embedding_lookup(self.embed_matrix, self.center_words, name='embed')

                # Step 4: 损失函数
                # NCE损失，权重和偏置
                nce_weight = tf.Variable(tf.truncated_normal([self.vocab_size, self.embed_size],
                                                            stddev=1.0 / (self.embed_size ** 0.5)), 
                                                            name='nce_weight')
                nce_bias = tf.Variable(tf.zeros([VOCAB_SIZE]), name='nce_bias')

                # nce损失函数
                self.loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weight, 
                                                    biases=nce_bias, 
                                                    labels=self.target_words, 
                                                    inputs=embed, 
                                                    num_sampled=self.num_sampled, 
                                                    num_classes=self.vocab_size), name='loss')
    def _create_optimizer(self):
        """ 优化器 """
        with tf.device('/cpu:0'):
            self.optimizer = tf.train.GradientDescentOptimizer(self.lr).minimize(self.loss, 
                                                              global_step=self.global_step)

    def _create_summaries(self):
        with tf.name_scope("summaries"):
            tf.summary.scalar("loss", self.loss)
            tf.summary.histogram("histogram loss", self.loss)
            # because you have several summaries, we should merge them all
            # into one op to make it easier to manage
            self.summary_op = tf.summary.merge_all()

    def build_graph(self):
        """ 模型图 """
        self._create_placeholders()
        self._create_embedding()
        self._create_loss()
        self._create_optimizer()
        self._create_summaries()

def train_model(model, batch_gen, num_train_steps, weights_fld):
    saver = tf.train.Saver() # defaults to saving all variables - in this case embed_matrix, nce_weight, nce_bias

    initial_step = 0
    utils.make_dir('w2v_exter_files/checkpoints')
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        ckpt = tf.train.get_checkpoint_state(os.path.dirname('w2v_exter_files/checkpoints/checkpoint'))
        # if that checkpoint exists, restore from checkpoint
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

        total_loss = 0.0 # we use this to calculate late average loss in the last SKIP_STEP steps
        writer = tf.summary.FileWriter('w2v_exter_files/improved_graph/lr' + str(LEARNING_RATE), sess.graph)
        initial_step = model.global_step.eval()
        for index in range(initial_step, initial_step + num_train_steps):
            centers, targets = next(batch_gen)
            feed_dict={model.center_words: centers, model.target_words: targets}
            loss_batch, _, summary = sess.run([model.loss, model.optimizer, model.summary_op], 
                                              feed_dict=feed_dict)
            writer.add_summary(summary, global_step=index)
            total_loss += loss_batch
            if (index + 1) % SKIP_STEP == 0:
                print('Average loss at step {}: {:5.1f}'.format(index, total_loss / SKIP_STEP))
                total_loss = 0.0
                saver.save(sess, 'checkpoints/skip-gram', index)
        
        ####################
        # code to visualize the embeddings. uncomment the below to visualize embeddings
        # run "'tensorboard --logdir='processed'" to see the embeddings
        # final_embed_matrix = sess.run(model.embed_matrix)
        
        # # it has to variable. constants don't work here. you can't reuse model.embed_matrix
        # embedding_var = tf.Variable(final_embed_matrix[:1000], name='embedding')
        # sess.run(embedding_var.initializer)

        # config = projector.ProjectorConfig()
        # summary_writer = tf.summary.FileWriter('processed')

        # # add embedding to the config file
        # embedding = config.embeddings.add()
        # embedding.tensor_name = embedding_var.name
        
        # # link this tensor to its metadata file, in this case the first 500 words of vocab
        # embedding.metadata_path = 'processed/vocab_1000.tsv'

        # # saves a configuration file that TensorBoard will read during startup.
        # projector.visualize_embeddings(summary_writer, config)
        # saver_embed = tf.train.Saver([embedding_var])
        # saver_embed.save(sess, 'processed/model3.ckpt', 1)

def main():
    model = SkipGramModel(VOCAB_SIZE, EMBED_SIZE, BATCH_SIZE, NUM_SAMPLED, LEARNING_RATE)
    model.build_graph()
    batch_gen = process_data(VOCAB_SIZE, BATCH_SIZE, SKIP_WINDOW)
    train_model(model, batch_gen, NUM_TRAIN_STEPS, WEIGHTS_FLD)
    
if __name__ == '__main__':
    main()