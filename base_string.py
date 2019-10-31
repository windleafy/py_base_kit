#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""base_string"""
# @Time    : 2019/10/31 12:59
# @Author  : Wind
# @Des     : 
# @Software: PyCharm  Python3.7.2
import random


def generate_random_str(random_length):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str
