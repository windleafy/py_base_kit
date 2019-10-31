#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 13:55
# @Author  : Wind
# @Site    : 
# @File    : base_requests.py
# @Software: PyCharm
import time
import random
import requests
import requests.adapters
from contextlib import closing

# url = 'https://www.baidu.com'


# requests.get读取页面
def get_html(url):
    # time.sleep(float(random.randint(1, 500)) / 100)

    """from requests.adapters import HTTPAdapter"""
    requests.adapters.DEFAULT_RETRIES = 5
    headers = {
        'Content-Type': "application/json;charset=uf8"
    }

    try:
        response = requests.get(url, headers=headers, stream=False, timeout=10)
    except Exception as e:
        print(e)
        print('html连接异常')
        return 'html_err'

    s = requests.session()
    s.keep_alive = False
    response.close()

    if response.status_code == 200:
        print(f'{url}\n页面请求成功')
        response.encoding = 'utf8'
        # print(type(response))    # <class 'requests.models.Response'>
        return response.text       # 输出网页文本
        # return response.json()   # 输入的地址内容是json
        # return response.content  # 输入的地址内容是文件，比如图片、视频
    else:
        print('请求网页源代码错误, 错误状态码：', response.status_code)
        return response.status_code


# requests.get下载方法
def download(url, save_name):
    # @ url  输入值，下载地址
    # @ save_name  输入值，文件保存名称
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False

    # noinspection PyBroadException
    try:
        # stream 设为 True，Requests 无法将连接释放回连接池
        # 使用以下closing方法处理
        with closing(requests.get(url, stream=True)) as response:
            print('连接状态：', response.status_code)
            if response.status_code != 200:
                print('\nnet_error1')
                time.sleep(5)
                return 'net_error1'
            content_size = int(response.headers['content-length'])  # 内容体总大小
            print('文件大小：', content_size / 1000, 'KB')

            chunk_size = 0x20000  # 单次请求最大值  0x20000=131072 bytes, default max ssl buffer size
            data_count = 0

            with open(save_name, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    # 下载存盘
                    file.write(data)

                    # 下载进度显示处理
                    data_count = data_count + len(data)
                    now_jd = (data_count / content_size) * 100
                    print('complete percent:%5.2f%s  %d : %d' % (now_jd, '%', data_count, content_size), end='\r')

                    # 下载完毕判定
                    if data_count / content_size == 1:
                        print('\n文件创建成功')
                        return 'download_success'

    except Exception as e:
        print('\nnet_error2')
        time.sleep(5)
        return 'net_error2'
