#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 14:04
# @Author  : Wind
# @Site    : 
# @File    : base_urlopen.py
# @Software: PyCharm


from urllib import request


def get_html(url):
    html = request.urlopen(url).read()
    html = html.decode('utf-8')
    print(html)
