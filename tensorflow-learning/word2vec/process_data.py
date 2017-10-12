#coding=utf-8

from collections import Counter
import random
import os
import sys
sys.path.append('..')
import zipfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

import utils

# Parameters for downloading data
DOWNLOAD_URL = 'http://mattmahoney.net/dc/'
EXPECTED_BYTES = 31344016
DATA_FOLDER = 'data/'
FILE_NAME = 'text8'

def download(file_name, expected_bytes):
    """ Download the dataset text8 if it's not already downloaded """
    file_path = DATA_FOLDER + file_name
    if os.path.exists(file_path):
        print("Dataset ready")
        return file_path
    print(DOWNLOAD_URL + file_name)
    file_name, _ = urllib.request.urlretrieve(DOWNLOAD_URL + file_name, file_path)
    
    file_stat = os.stat(file_path)
    if file_stat.st_size == expected_bytes:
        print('Successfully downloaded the file', file_name)
    else:
        raise Exception('File ' + file_name +
                        ' might be corrupted. You should try downloading it with a browser.')
    return file_path

def read_data(file_path):
    """ 
    大约有17,005,207词（含标点符号）
    把所有的词读进一个list中，英文是空格分割，含标点符号，
    """
    with zipfile.ZipFile(file_path) as f:
        words = tf.compat.as_str(f.read(f.namelist()[0])).split() 
        # tf.compat.as_str() 输入的转换成string
    return words

def build_vocab(words, vocab_size):
    """ Build vocabulary of VOCAB_SIZE most frequent words 
    建立字典，给定的vocab_size大小，建立；按照频率选取前vocab_size个词，
    返回词的索引，数组和字典，
    """
    dictionary = dict()
    count = [('UNK', -1)]
    count.extend(Counter(words).most_common(vocab_size - 1))
    index = 0
    utils.make_dir('processed')
    with open('processed/vocab_1000.tsv', "w") as f:
        for word, _ in count:
            dictionary[word] = index
            if index < 1000:
                f.write(word + "\n")
            index += 1
    index_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return dictionary, index_dictionary

def convert_words_to_index(words, dictionary):
    """ 
    把词替换成词典中的索引
    """
    return [dictionary[word] if word in dictionary else 0 for word in words]

def generate_sample(index_words, context_window_size):
    """ 
    skip-gram模型，生成训练对，
    
     """
    for index, center in enumerate(index_words):
        context = random.randint(1, context_window_size)
        # 随机选择中心词的前一个后一个，还是前几个后几个，
        for target in index_words[max(0, index - context): index]:
            yield center, target
        # get a random target after the center wrod
        for target in index_words[index + 1: index + context + 1]:
            yield center, target

def get_batch(iterator, batch_size):
    """ Group a numerical stream into batches and yield them as Numpy arrays. """
    while True:
        center_batch = np.zeros(batch_size, dtype=np.int32)
        target_batch = np.zeros([batch_size, 1])
        for index in range(batch_size):
            center_batch[index], target_batch[index] = next(iterator)
            #next是从迭代器中挨个取值，这里是词对，生成的词对
            #中心词索引-->前skip个（后skip个）词索引，这样的对，
        yield center_batch, target_batch

def process_data(vocab_size, batch_size, skip_window):
    #file_path = download(FILE_NAME, EXPECTED_BYTES)
    file_path = "E:/workspace/DeepLearnings/tensorflow-learning/data/text8.zip"
    print(file_path)
    words = read_data(file_path)#读取训练所有词，存储在一个list中，
    dictionary, _ = build_vocab(words, vocab_size)#建立词典，根据指定的词典大小，词典的构建依赖于词在训练样本中的频率
    index_words = convert_words_to_index(words, dictionary)#得到词典，把训练集替换成索引，即文字-->数字
    del words # 词存入内存
    single_gen = generate_sample(index_words, skip_window)#获取样本，根据中心词选取前后skip个词，构成词对，
    return get_batch(single_gen, batch_size)

def get_index_vocab(vocab_size):
    file_path = download(FILE_NAME, EXPECTED_BYTES)
    words = read_data(file_path)
    return build_vocab(words, vocab_size)