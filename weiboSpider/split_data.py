# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
import jieba
import pickle
from tqdm import tqdm
from collections import Counter

with open('split_data.pkl', 'rb') as f:
    split_data = pickle.load(f)

with open('stop_words.txt', 'r', encoding='utf-8') as f:
    stop_word = f.read()

stop_word = stop_word.split('\n')

split_word = [[] for _ in range(4)]

for i in range(4):
    each_split = split_data[i]
    for each_data in tqdm(each_split, desc='分词'):
        cut_res = list(jieba.cut(each_data[0]))
        for each in cut_res:
            if each in stop_word:
                continue
            if each == ' ':
                continue
            split_word[i].append(each)

for i in tqdm(range(4), desc='统计词频'):
    tmp_dict = Counter(split_word[i])
    for each in sorted(tmp_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        with open(str(i) + '.txt', 'a', encoding='utf-8') as f:
            f.write(str(each[0]) + '\t' + str(each[1]) + '\n')
print()
