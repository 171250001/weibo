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

# 2019-12.8-2020.1.22    2019.12.8-2020.1.22
# 2020.1.23-2020.2.7    2020.1.23-2020.2.9
# 2020.2.10-2020.2.13   2020.2.10-2020.3.9
# 2020.3.10-2020.6      2020.3.10-2020.6.15

import time
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']

res_emotion = pd.read_csv('res_emotion.csv')
res_emotion = res_emotion.values.tolist()

split_list = [[] for _ in range(4)]

positive_number = [0, 0, 0, 0]
mid_number = [0, 0, 0, 0]
negative_number = [0, 0, 0, 0]

split_flag = [0, 0, 0, 0]

# 110 6241 9641 20005
s_t = time.strptime('2020-1-22', '%Y-%m-%d')
split_flag[0] = time.mktime(s_t)
s_t = time.strptime('2020-2-9', '%Y-%m-%d')
split_flag[1] = time.mktime(s_t)
s_t = time.strptime('2020-3-9', '%Y-%m-%d')
split_flag[2] = time.mktime(s_t)
s_t = time.strptime('2020-6-15', '%Y-%m-%d')
split_flag[3] = time.mktime(s_t)

split_res = [0, 0, 0, 0]

for each in res_emotion:
    s = each[4].split()[0]
    s_t = time.strptime(s, '%Y-%m-%d')
    a_i = time.mktime(s_t)
    if a_i <= split_flag[0]:
        split_list[0].append([each[2], each[3], each[4], each[5]])
        split_res[0] += each[5]
        if each[5] < 0.33:
            negative_number[0] += 1
        elif each[5] < 0.66:
            mid_number[0] += 1
        else:
            positive_number[0] += 1
    elif a_i <= split_flag[1]:
        split_list[1].append([each[2], each[3], each[4], each[5]])
        split_res[1] += each[5]
        if each[5] < 0.33:
            negative_number[1] += 1
        elif each[5] < 0.66:
            mid_number[1] += 1
        else:
            positive_number[1] += 1
    elif a_i <= split_flag[2]:
        split_list[2].append([each[2], each[3], each[4], each[5]])
        split_res[2] += each[5]
        if each[5] < 0.33:
            negative_number[2] += 1
        elif each[5] < 0.66:
            mid_number[2] += 1
        else:
            positive_number[2] += 1
    elif a_i <= split_flag[3]:
        split_list[3].append([each[2], each[3], each[4], each[5]])
        split_res[3] += each[5]
        if each[5] < 0.33:
            negative_number[3] += 1
        elif each[5] < 0.66:
            mid_number[3] += 1
        else:
            positive_number[3] += 1

for i in range(4):
    split_res[i] = split_res[i] / len(split_list[i])
    positive_number[i] = positive_number[i] / len(split_list[i])
    negative_number[i] = negative_number[i] / len(split_list[i])
    mid_number[i] = mid_number[i] / len(split_list[i])

with open('split_data.pkl', 'wb') as f:
    pickle.dump(split_list, f)

print(positive_number)
print(negative_number)
print(mid_number)
print(split_res)

x = ['2020-01-22', '2020-02-09', '2020-03-09', '2020-06-15']
plt.plot(split_res)
plt.title('情感得分变化')
plt.xticks(range(5), x)
plt.xlabel('日期')
plt.ylabel('平均情感得分')
for i in range(4):
    plt.text(i, split_res[i] + 0.0005, '%.4f' % split_res[i], ha='center', va='bottom', fontsize=9)
plt.savefig('情感得分变化.jpg')
plt.show()

x = ['2020-01-22', '2020-02-09', '2020-03-09', '2020-06-15']
plt.plot(positive_number, c='g')
plt.plot(negative_number, c='r')
plt.plot(mid_number, c='y')
plt.legend(['积极', '消极', '中性'])
plt.title('积极情感比例')
plt.xticks(range(5), x)
plt.xlabel('日期')
plt.ylabel('积极比例（%）')
for i in range(4):
    plt.text(i, positive_number[i] + 0.0005, '%.4f' % positive_number[i], ha='center', va='bottom', fontsize=9,
             color='g')
    plt.text(i, negative_number[i] + 0.0005, '%.4f' % negative_number[i], ha='center', va='bottom', fontsize=9,
             color='r')
    plt.text(i, mid_number[i] + 0.0005, '%.4f' % mid_number[i], ha='center', va='bottom', fontsize=9, color='y')
plt.savefig('积极情感比例.jpg')

plt.show()
