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
import pymongo
from tqdm import tqdm


def get_data():
    client = pymongo.MongoClient('mongodb://server2.sniper97.cn:27777')
    db = client['weibo']
    col = db['weibo']
    res = []
    data = col.find()
    print('find')
    data = list(data)
    print('change')
    for each in tqdm(data):
        if '新冠' in each['content'] or '疫' in each['content']:
            res.append([each['id'], each['content'], each['publish_time']])
    with open('db_data.pkl', 'wb') as f:
        pickle.dump(res, f)
    return res


def get_saved_data():
    with open('db_data.pkl', 'rb') as f:
        res = pickle.load(f)
    return res


if __name__ == '__main__':
    get_saved_data()
