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

import codecs
import os

import jieba.analyse
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 要提取关键词的文本所在文件夹
base_path = "data"
# 分词后的文本保存的文件位置
seg_path = "segmented/"


def segment():
    for txt in os.listdir(base_path):
        whole_base = os.path.join(base_path, txt)
        whole_seg = os.path.join(seg_path, txt)
        with codecs.open(whole_base, 'r', 'utf-8') as fr:
            fw = codecs.open(whole_seg, 'w', 'utf-8')
            for line in fr.readlines():
                seg_list = jieba.analyse.extract_tags(line.strip(), topK=50, withWeight=False, allowPOS=())
                fw.write(" ".join(seg_list))
                # seg_list = jieba.analyse.extract_tags(line.strip(), topK=50, withWeight=True, allowPOS=())
                # res = []
                # for seg in seg_list:
                #     res.append(str(seg[0]) + '\t' + str(seg[1]) + '\n')
                # fw.writelines(" ".join(res))
            fw.close()


def read_doc_list():
    trade_list = []
    doc_list = []
    for txt in os.listdir(seg_path):
        trade_list.append(txt.split(".")[0])
        with codecs.open(os.path.join(seg_path, txt), "r", "utf-8") as fr:
            doc_list.append(fr.read().replace('\n', ''))
    return trade_list, doc_list


def tfidf_top(trade_list, doc_list, max_df, topn):
    vectorizer = TfidfVectorizer(max_df=max_df)
    matrix = vectorizer.fit_transform(doc_list)
    feature_dict = {v: k for k, v in vectorizer.vocabulary_.items()}  # index -> feature_name
    top_n_matrix = np.argsort(-matrix.todense())[:, :topn]  # top tf-idf words for each row
    df = pd.DataFrame(np.vectorize(feature_dict.get)(top_n_matrix), index=trade_list)  # convert matrix to df
    return df


segment()
tl, dl = read_doc_list()
tdf = tfidf_top(tl, dl, max_df=0.5, topn=20)
tdf.to_csv("keywords.txt", header=False, encoding='utf-8')
