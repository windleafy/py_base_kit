#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""base_mysql"""
# @Time    : 2019/10/30 9:45
# @Author  : Wind
# @Des     : 
# @Software: PyCharm  Python3.7.2
from pymysql import connect


class MysqlPython:
    def __init__(self, host, port, user, pwd, charset="utf8"):
        self.host = host
        self.port = port
        # self.db = db
        self.user = user
        self.pwd = pwd
        self.charset = charset

        # 初始化连接
        self._conn = self.get_connect()
        if self._conn:
            self._cur = self._conn.cursor()
            print('服务器连接成功！')

        self._db_name = ''
        self._table_name = ''

    # 建立数据库连接(初始化会调用，不需要单独使用)
    def get_connect(self):
        try:
            conn = connect(
                host=self.host, port=self.port,
                user=self.user, password=self.pwd, charset=self.charset)
        except Exception as e:
            print(f'服务器连接失败{e}')
        else:
            return conn

    # 获取连接信息
    def get_conn_info(self):
        print("连接信息：")
        print(f"服务器:{self.host} , 用户名:{self.user}")

    # 打开数据库
    def open_db(self, db_name):
        pass
        try:
            self._cur.execute(f"USE {db_name}")
        except Exception as e:
            print(e)
            print(f'{db_name}打开失败！')
        else:
            self._db_name = db_name
            print(f'打开数据库{db_name}完成')

    # 关闭数据库连接
    def close(self):
        if self._conn:
            try:
                self._cur.close()
                print(f'数据库{self._db_name}关闭成功！')
                self._conn.close()
                print('服务器连接关闭成功！')
            except Exception:
                raise ("关闭异常, %s,%s" % (type(self._cur), type(self._conn)))

    # 执行查询
    def exec_query(self, sql):
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res

    # 执行非查询类语句
    def exec_non_query(self, sql):
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
            print('数据提交成功!')
        except Exception as err:
            flag = False
            self._conn.rollback()
            print(f"执行失败, {err}")
        else:
            return flag

    # 创建数据库
    def create_db(self, db_name):
        sql = f"CREATE DATABASE {db_name};"
        try:
            self._cur.execute(sql)
        except Exception as e:
            print(e)
        else:
            print(f'数据库{db_name}创建完成')

    # 创建数据表
    def create_table(self, db_name, target_table):
        self._cur.execute(f"use {db_name}")
        print(f'打开数据库{db_name}完成')
        try:
            self._cur.execute(target_table)
        except Exception as e:
            print(e)
        else:
            table_name = target_table.split('`')[1]
            print(f'数据表{table_name}创建完成')
