#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019-09-07 22:50
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : spider.py
import json
import re
import time

import requests
from requests.exceptions import RequestException
from multiprocessing import Pool


def get_one_page(url):
    try:
        response = requests.get(url)
        # while response.status_code != 200:
        #     response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print('状态码：', response.status_code, url)
            while response.status_code != 200:  # 如果状态码不是 200，就一直发起请求，直到状态码为 200 为止
                response = requests.get(url)
            print('状态码：', response.status_code, url)
            return response.text
    except RequestException as e:
        print('错误:', e)
        return


def parse_one_page(html):
    pattern = re.compile('<dd>.*?'
                         # + '<i class="board-index(.*?)">(.*?)</i>.*?'  # 序号
                         + '<i class="board-index board-index-.*?">(.*?)</i>.*?'  # 序号
                         + 'data-src="(.*?)".*?'  # 图片地址
                         + 'name"><a.*?>(.*?)</a>.*?'  # 标题
                         + '<p class="star">(.*?)</p>.*?'  # 演员
                         + '<p class="releasetime">(.*?)</p>.*?'  # 时间
                         + '<i class="integer">(.*?)</i>.*?'  # 评分
                         + '<i class="fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    """
    :param content:dict
    :return:
    """
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False))
        f.write('\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    if html is not None:
        for item in parse_one_page(html):
            write_to_file(item)
    else:
        print('None')


if __name__ == '__main__':
    t1 = time.time()
    # 单线程
    # for i in range(10):
    #     main(i * 10)

    # 多线程
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
    t2 = time.time()
    print(t2 - t1)
