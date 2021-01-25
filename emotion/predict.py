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
import tensorflow as tf
from utils import get_token
from bert_fc import Bert
from transformers import BertTokenizer
from read_excel_all import read_excel
from wirte_excel import write_excel

for gpu in tf.config.experimental.list_physical_devices('GPU'):
    tf.config.experimental.set_memory_growth(gpu, True)

excel_data = read_excel('res.xlsx', 'Sheet1', [0, 1, 2, 3], False)
text = []
for each in excel_data:
    each[3] = str(each[3])
    each[1] = str(each[1])
    if each[1] is not None:
        text.append(each[1])
    else:
        text.append('')

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
test_X = get_token(text, 140, tokenizer)

model = Bert()
optimizer = tf.keras.optimizers.Adam(1e-6)
model.compile(optimizer=optimizer, loss=tf.keras.losses.categorical_crossentropy, metrics=['acc'])

try:
    model.load_weights('output/model.ckpt')
    print('load saved model')
except:
    print('train model for init')

res = model.predict(test_X, verbose=1)
res = list(res[:, 1])


data = []
for i in range(len(excel_data)):
    each = excel_data[i]
    each.append(res[i])
    data.append(each)

import pandas as pd

data = pd.DataFrame(columns=['发布者主页', '评论内容', '点赞数量', '发布时间', '情感打分'],
                    data=data)
data.to_csv('res_emotion.csv', encoding='utf-8')
# write_excel('res_emotion_' + user_id + '.xlsx', data, col_name_list=['发布时间', '微博正文', '情感打分'])

print()
