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
import pickle
import os
from tqdm import tqdm
import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer
from sklearn.model_selection import train_test_split


def read_file():
    data = pd.read_csv('data/weibo_senti_100k.csv', encoding='utf-8', )
    labels = list(data['label'])
    texts = list(data['review'])
    return texts, labels

def get_token(data_list, token_length, tokenizer):
    temp_ids = []
    temp_mask = []
    temp_token = []
    for i in tqdm(range(len(data_list)), desc='get token'):
        temp = tokenizer.encode_plus(data_list[i], max_length=token_length,
                                     truncation='longest_first',
                                     padding='max_length')

        temp_ids.append(temp['input_ids'])
        temp_mask.append(temp['attention_mask'])
        temp_token.append(temp['token_type_ids'])

    temp_ids = np.asarray(temp_ids, dtype=np.int32)
    temp_mask = np.asarray(temp_mask, dtype=np.int32)
    temp_token = np.asarray(temp_token, dtype=np.int32)
    text_list = [temp_ids, temp_mask, temp_token]
    return text_list


def get_data():
    if os.path.exists('./data.dat'):
        with open('data.dat', 'rb') as f:
            data = pickle.load(f)
        return data['train_X'], data['train_y'], data['val_X'], data['val_y']
    else:
        texts, labels = read_file()
        train_X, val_X, train_y, val_y = train_test_split(texts, labels, test_size=0.2)

        train_X = train_X[:10000]
        val_X = val_X[:1000]
        train_y = train_y[:10000]
        val_y = val_y[:1000]

        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        train_X = get_token(train_X, 140, tokenizer)
        val_X = get_token(val_X, 140, tokenizer)
        train_y = tf.keras.utils.to_categorical(train_y, num_classes=2)
        val_y = tf.keras.utils.to_categorical(val_y, num_classes=2)
        data = {
            'train_X': train_X,
            'train_y': train_y,
            'val_X': val_X,
            'val_y': val_y
        }
        with open('data.dat', 'wb') as f:
            pickle.dump(data, f)
        return train_X, train_y, val_X, val_y


if __name__ == '__main__':
    get_data()
