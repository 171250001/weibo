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

import requests

requests.packages.urllib3.disable_warnings()
from lxml import etree

from datetime import datetime, timedelta

import csv

from math import ceil

import re
from time import sleep
from random import randint

from read_mongo import get_saved_data

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': '''ALF=1614001984; SCF=ApnAj28PkcpY6Zea_EUCT4DP9Y3pBwEXqonge2sSrPUX1ULd35T0JEq-Law9Y_ky0UtcWKCSw9pOX9-H5w_haa8.; _T_WM=11455681572; SUB=_2A25NCFoQDeRhGeNP6VEV-CvIzTSIHXVu82ZYrDV6PUJbktANLXjgkW1NTjbySgMM8lYY9ZvxwJ3GiRqDJLFrmVgO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh1kpXcUgLAHDsQ1MaIEpzE5JpX5K-hUgL.Fo-peoeX1h-XSon2dJLoIXMLxKBLBonL1h5LxKBLBonLB-2LxKqLBozLBK2LxKqL1-eL1h.LxKqL1hBL1-qLxKqL1heL1h-LxKML1-2L1hx_qgSQIg4LP7tt; SSOLoginState=1611409984; WEIBOCN_FROM=1110006030; XSRF-TOKEN=23da0e; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4596892359723920%26luicode%3D10000011%26lfid%3D1076032656274875%26uicode%3D20000061%26fid%3D4596892359723920'''
}


def parse_time(publish_time):
    publish_time = publish_time.split('来自')[0]
    if '刚刚' in publish_time:
        publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    elif '分钟' in publish_time:
        minute = publish_time[:publish_time.find('分钟')]
        minute = timedelta(minutes=int(minute))
        publish_time = (datetime.now() -
                        minute).strftime('%Y-%m-%d %H:%M')
    elif '今天' in publish_time:
        today = datetime.now().strftime('%Y-%m-%d')
        time = publish_time[3:]
        publish_time = today + ' ' + time
    elif '月' in publish_time:
        year = datetime.now().strftime('%Y')
        month = publish_time[0:2]
        day = publish_time[3:5]
        time = publish_time[7:12]
        publish_time = year + '-' + month + '-' + day + ' ' + time
    else:
        publish_time = publish_time[:16]
    return publish_time


def get_one_comment_struct(comment):
    # xpath 中下标从 1 开始
    userURL = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])

    content = comment.xpath(".//span[@class='ctt']/text()")
    # '回复' 或者只 @ 人
    if '回复' in content or len(content) == 0:
        test = comment.xpath(".//span[@class='ctt']")
        content = test[0].xpath('string(.)').strip()

        # 以表情包开头造成的 content == 0,文字没有被子标签包裹
        if len(content) == 0:
            content = comment.xpath('string(.)').strip()
            content = content[content.index(':') + 1:]
    else:
        content = content[0]

    if ' ' in content:
        return None

    praisedNum = comment.xpath(".//span[@class='cc'][1]/a/text()")[0]
    praisedNum = praisedNum[2:praisedNum.rindex(']')]

    publish_time = comment.xpath(".//span[@class='ct']/text()")[0]

    publish_time = parse_time(publish_time)
    # nickName,sex,location,weiboNum,followingNum,followsNum = self.getPublisherInfo(url=userURL)

    return [userURL, content, praisedNum, publish_time]


def write_to_csv(result):
    with open('comments.csv', 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result)
    # print('已成功将{}条评论写入{}中'.format(len(result), 'comments.csv'))


def run(wid):
    from tqdm import tqdm

    # res = requests.get('https://weibo.cn/comment/{}'.format(wid), headers=headers, verify=False)
    # commentNum = re.findall("评论\[.*?\]", res.text)[0]
    # commentNum = int(commentNum[3:len(commentNum) - 1])
    # print(commentNum, end='\t')
    # pageNum = ceil(commentNum / 10)
    # print(pageNum)
    for page in (range(1)):
        result = []

        try:
            res = requests.get('https://weibo.cn/comment/{}?page={}'.format(wid, page + 1), headers=headers,
                               verify=False)
        except:
            sleep(5)
            try:
                res = requests.get('https://weibo.cn/comment/{}?page={}'.format(wid, page + 1), headers=headers,
                                   verify=False)
            except:
                sleep(10)

                res = requests.get('https://weibo.cn/comment/{}?page={}'.format(wid, page + 1), headers=headers,
                                   verify=False)

        html = etree.HTML(res.text.encode('utf-8'))

        comments = html.xpath("/html/body/div[starts-with(@id,'C')]")

        # print('第{}/{}页'.format(page + 1, pageNum))

        for i in range(len(comments)):
            res = get_one_comment_struct(comments[i])
            if res is not None:
                result.append(res)

        write_to_csv(result)

        sleep(randint(1, 5))


def start():
    data = get_saved_data()
    from tqdm import tqdm
    for i in tqdm(range(0, len(data))):
        try:
            run(data[i][0])
        except:
            print('error')
            continue


if __name__ == '__main__':
    start()
