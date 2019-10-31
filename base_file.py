#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/28 16:27
# @Author  : Wind
# @Des     : 文件相关操作
# @Site    : 
# @File    : base_file.py
# @Software: PyCharm
import os
import csv
import json


# 创建存盘路径
def dir_chk_create(file_path):
    """
    :param file_path: 要检查的路径
    """
    # @ file_path：
    path_exist = os.path.exists(file_path)  # 如果目录不存在，则创建目录
    if path_exist:
        print(f'{file_path}目录已存在!\n')
    else:
        os.makedirs(file_path)
        print(f'{file_path}目录创建成功\n')


# 将dict保存到json文件
def json2file(data, save_path, save_name):
    """
    :param data: 要保存的json字典字符串数据列表json.dumps(my_json)
    :param save_path: 保存的路径
    :param save_name: 保存的文件名
    """

    path_exist = os.path.exists(save_path)  # 如果目录不存在，则创建目录
    if path_exist:
        print('目录已存在，准备输出文件')
    else:
        os.makedirs(save_path)
        print(f'{save_path}目录创建成功')

    with open(save_path + save_name, 'w', encoding='utf_8') as json_file:
        json_file.write(data)
    print(f'{save_name}保存完毕')


# 将str_list保存到文件
def str_list2csv(data, save_path, save_name):
    """
    把一个字符串列表存入文件，列表的item:  ','.join(seq)
    格式:['str1_1,str1_2,str1_3','str2_1,str2_2,str2_3','str3_1,str3_2,str3_3']
    :param data:要保存的字符串列表
    :param save_path:保存的路径
    :param save_name:保存的文件名
    """
    path_exist = os.path.exists(save_path)  # 如果目录不存在，则创建目录
    if path_exist:
        pass
        print(f'{save_path}目录已存在，准备输出文件')
    else:
        os.makedirs(save_path)
        print(f'{save_path}目录创建成功，准备输出文件')

    with open(save_path + save_name, 'a', newline='', encoding='utf_8') as txt_file:
        for item in data:
            txt_file.writelines(item + '\n')
    print(f'{save_name}保存完毕!\n')


# 将str_list组成的list保存到csv文件
def list2csv(data):
    """
    :param data: data.save_name
    :param data: data.header
    :param data: data.rows  [[str1_1,str1_2,str1_3],[str2_1,str2_2,str2_3],[str3_1,str3_2,str3_3]]
    """
    name = data.save_name.split('/')[-1]
    pos = data.save_name.find(name)
    path = data.save_name[0:pos]
    dir_exist = os.path.exists(path)
    if dir_exist:
        pass
        print(f'{path}目录已存在，准备输出文件')
    else:
        os.mkdir(path)
        print('目录创建成功，准备输出文件')

    file_exist = os.path.exists(data.save_name)
    with open(data.save_name, 'a', newline='', encoding='utf_8') as f:
        f_csv = csv.writer(f)
        if not file_exist:
            f_csv.writerow(data.header)
        f_csv.writerows(data.rows)
        print(f'{data.save_name}输出完毕\n')


# 将dict_list保存到csv文件
def dict_list2csv(data):
    """
    :param data: data.file_path:文件保存路径
    :param data: data.file_name:文件保存名称
    :param data: data.header;数据表头
    :param data: data.rows:字典数据列表
    """
    # print(f'path:{data.file_path}')
    path_exist = os.path.exists(data.file_path)  # 如果目录不存在，则创建目录
    if path_exist:
        print('目录已存在，准备输出文件')
    else:
        os.makedirs(data.file_path)
        print(f'{data.file_path}目录创建成功')

    file_exist = os.path.exists(data.file_path+data.file_name)  # 如果文件不存在，则创建表头
    with open(data.file_path + data.file_name, 'a', newline='', encoding='utf_8') as f:
        f_csv = csv.DictWriter(f, data.header)
        if not file_exist:
            f_csv.writeheader()
        f_csv.writerows(data.rows)
        print(f'{data.file_name}输出完毕!')


# 读取csv文件内容至list变量
def csv2list(file_path):
    """
    :param file_path: 读取的csv文件
    :return: header,返回表头
    :return:  list(f_csv),返回数据列表
    """
    # @ file_path:
    # @ header   :返回表头
    # @ list(f_csv):返回表内容
    with open(file_path) as f:
        f_csv = csv.reader(f)
        header = next(f_csv)
        return header, list(f_csv)


# 读取json文件内容至字典变量
def json_file2dict(file_path):
    """
    :param file_path: 读取的json文件
    :return: 返回一个字典
    """
    with open(file_path, encoding='utf_8') as f:
        return json.load(f)
