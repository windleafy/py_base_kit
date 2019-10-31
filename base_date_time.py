#!/usr/bin/env python
"""base_date_time"""
# -*- coding: utf-8 -*-
# @Time    : 2019/10/7 22:04
# @Author  : Wind
# @Des     : 
# @Software: PyCharm
from datetime import datetime, timedelta

# 中文星期值字典
week_dict_cn = {6: '星期日', 0: '星期一', 1: '星期二',
                2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六'}


# 输入距今天的日期差，返回对应日期值
def getdate_off_today(x):
    """
    :param x:与今天的日期差
    :return:返回日期值
    """
    return (datetime.today() + timedelta(days=x)).strftime('%Y-%m-%d')


# 输入距今天的日期差，返回中文星期值
def get_weekday_off_today(x):
    """
    :param x: 与今天的日期差
    :return:返回星期值
    """
    week_day = (datetime.now() + timedelta(days=x)).weekday()
    return week_dict_cn.get(week_day)


# 输入指定日期，返回中文星期值
def get_weekday(date):
    """
    :param date:输入指定日期'2019-01-02'
    :return: 返回指定日期的星期值
    """
    week_key = datetime.strptime(date, '%Y-%m-%d').weekday()
    return week_dict_cn.get(week_key)


# 输入两个日期值，返回日期差值
def date_diff(x, y):
    """
    :param x: 前一日期值
    :param y: 后一日期值
    :return:日期差值
    """
    date1 = datetime.strptime(x, '%Y-%m-%d')
    date2 = datetime.strptime(y, '%Y-%m-%d')
    return (date2 - date1).days


def test():
    """
    测试区
    """
    dt_string = "2002-01-14 09:15:32"
    # 字符串转日期对象
    dt_object = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")

    print(dt_object.strftime('%c'))
    print(dt_object.strftime('%F %T'))
    print(dt_object.strftime('%D'))

    print('\n年')
    print(dt_object.strftime('%Y'))
    print(dt_object.strftime('%C'))
    print(dt_object.strftime('%g'))
    print(dt_object.strftime('%G'))

    print('\n星期')
    print(dt_object.strftime('%w'))
    print(dt_object.strftime('%a'))
    print(dt_object.strftime('%A'))

    print('\n月份')
    print(dt_object.strftime('%h'))
    print(dt_object.strftime('%b'))
    print(dt_object.strftime('%B'))

    print('\n日期')
    print(dt_object.strftime('%d'))
    print(dt_object.strftime('%e'))
    print(dt_object.strftime('%j'))


if __name__ == '__main__':
    test()
