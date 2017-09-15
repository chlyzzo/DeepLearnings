#coding=utf-8
'''
Created on 2017-09-11

@author: wenhaohu
'''

import tensorflow as tf
import numpy as np
import pickle,os

#加载训练好的模型数据，
#加载语料数据，
corpus_int,vocab_to_int,int_to_vocab,token_dict = pickle.load(open('./myData/train_ing_data/preprocess.p',mode='rb'))
seq_length,save_dir = pickle.load(open('./myData/train_ing_data/params.p',mode='rb'))

#使用训练好的模型，生成结果，
#首先随机选词，提供开头
def pick_word(probabilities,int_to_vocab):
    
    '''
    随机选取下一个词
    下一个词的概率分布，
    词典与词索引对应关系
    返回基于当前预测的下一个词
    '''
    return np.random.choice(list(int_to_vocab.values()),1,p=probabilities)[0]
#加载图并开始生成

gen_length = 1000
prime_words = 'daenerys'

loaded_graph = tf.Graph()
with tf.Session(graph=loaded_graph) as sess:
    #加载保存的模型，已经训练好的
    loader = tf.train.import_meta_graph(save_dir+'.meta')
    loader.restore(sess, save_dir)
    
    #从加载的模型中获取张量，即各个训练好的参数
    input_text = loaded_graph.get_tensor_by_name('input:0')
    initial_state = loaded_graph.get_tensor_by_name('initial_state:0')
    final_state = loaded_graph.get_tensor_by_name('final_state:0')
    probs = loaded_graph.get_tensor_by_name('probs:0')
    
    #句子生成设置
    gen_sentences = prime_words.split()
    prev_state = sess.run(initial_state,{input_text:np.array([[1 for word in gen_sentences]])})    
    
    #生成句子
    for n in range(gen_length):
        #动态输入
        dyn_input = [[vocab_to_int[word] for word in gen_sentences[-seq_length:]]]
        dyn_seq_length = len(dyn_input[0])
        
        #获得词预测
        probabilities,prev_state = sess.run(
            [probs,final_state],
            {input_text:dyn_input,initial_state:prev_state}
            )
        
        pred_word = pick_word(probabilities[dyn_seq_length-1], int_to_vocab)
        
        gen_sentences.append(pred_word)
        
    #删除切割词
    chapter_text = ' '.join(gen_sentences)
    
    for key,token in token_dict.items():
        chapter_text = chapter_text.replace(' '+token.lower(),key)
        
    print(chapter_text)

    #结果的处理，替换些词
    chapter_text = chapter_text.replace('\n ', '\n')
    chapter_text = chapter_text.replace('( ', '(')
    chapter_text = chapter_text.replace(' ”', '”')
    capitalize_words = ['lannister', 'stark', 'lord', 'ser', 'tyrion', 'jon', 'john snow', 'daenerys', 'targaryen', 'cersei', 'jaime', 'arya', 'sansa', 'bran', 'rikkon', 'joffrey', 
                    'khal', 'drogo', 'gregor', 'clegane', 'kings landing', 'winterfell', 'the mountain', 'the hound', 'ramsay', 'bolton', 'melisandre', 'shae', 'tyrell',
                   'margaery', 'sandor', 'hodor', 'ygritte', 'brienne', 'tarth', 'petyr', 'baelish', 'eddard', 'greyjoy', 'theon', 'gendry', 'baratheon', 'baraTheon',
                   'varys', 'stannis', 'bronn', 'jorah', 'mormont', 'martell', 'oberyn', 'catelyn', 'robb', 'loras', 'missandei', 'tommen', 'robert', 'lady', 'donella', 'redwyne'
                   'myrcella', 'samwell', 'tarly', 'grey worm', 'podrick', 'osha', 'davos', 'seaworth', 'jared', 'jeyne poole', 'rickard', 'yoren', 'meryn', 'trant', 'king', 'queen',
                   'aemon']
    
    for word in capitalize_words:
        chapter_text = chapter_text.replace(word, word.lower().title())

    #保存文件
    version_dir = './myData/train_ing_data/generated-book-v1'
    if not os.path.exists(version_dir):
        os.makedirs(version_dir)

    num_chapters = len([name for name in os.listdir(version_dir) if os.path.isfile(os.path.join(version_dir, name))])
    file_id = str(num_chapters + 1)
    next_chapter = version_dir + '/chapter-' + file_id + '.md'
    with open(next_chapter, "w",encoding='utf-8') as text_file:
        text_file.write(chapter_text)
    
    
    