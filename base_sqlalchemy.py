#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""base_sqlalchemy"""
# @Time    : 2019/11/1 15:22
# @Author  : Wind
# @Des     : 自定义sqlalchemy类
# @Software: PyCharm  Python3.7.2
import re
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database, table_name


class MySqlAlchemy:
    # 初始化
    def __init__(self, host, port, user, pwd, db_name):
        self._uri = 'mysql+pymysql://' + user + ':' + pwd \
                    + '@' + host + ':' + port + '/' + db_name
        self.db_name = db_name
        self._engine = create_engine(
            self._uri,
            max_overflow=2,  # 超过连接池大小外最多创建的数量,
            pool_size=5,  # 连接池的大小
            pool_timeout=30,  # 池中没有线程最多等待的时间
            pool_recycle=-1,  # 多久之后对线程中的线程进行一次连接的回收(重置)
        )

    # 检查数据库是否存在
    def db_exist(self):
        return database_exists(self._engine.url)

    # 创建数据库
    def crt_db(self):
        if not self.db_exist():
            create_database(self._engine.url)
            print('数据库创建成功')
        else:
            print('数据库已存在')

    # 删除数据库
    def drop_db(self):
        if not self.db_exist():
            print('数据库不存在')
        else:
            drop_database(self._engine.url)
            print('数据库已删除')

    # 创建表
    def crt_tb(self, base):
        status = self.db_status_chk(base)
        if status == 2:
            # 创建指定表
            tables = [base.metadata.tables[table_name(base)]]
            base.metadata.create_all(self._engine, tables)
            print('数据表创建成功！')
        elif status == 4:
            print('数据表已存在！')

    # 删除表
    def drop_tb(self, base):
        status = self.db_status_chk(base)
        if status == 4:
            tables = [base.metadata.tables[table_name(base)]]
            base.metadata.drop_all(self._engine, tables)
            print('数据表删除成功')
        elif status == 2:
            print('数据表不存在！')

    # 检查数据库和数据表是否存在
    def db_status_chk(self, base):
        """
        检查数据库是否存在，数据表是否存在
        """
        pass
        try:
            metadata = MetaData(self._engine)
            # 通过反射，判断表是否已存在
            Table(table_name(base), metadata, autoload=True)
        except Exception as ex:
            if re.search('Unknown database', str(ex)):
                print('数据库不存在!')
                return 1
            elif str(ex) == f'`{table_name(base)}`':  # 数据表不存在时，返回的是表名
                return 2
            else:
                print(ex)  # 其它未知异常输出
                return 3
        else:
            # 数据表已存在
            return 4

    # 创建session
    def crt_session(self, base):
        status = self.db_status_chk(base)
        if status == 1:  # 数据库不存在
            return False
        elif status == 2:
            print('数据表不存在！')
            return False
        elif status == 3:  # 未知错误
            return False

        elif status == 4:
            # 数据表存在，创建session
            DBSession = sessionmaker(bind=self._engine)
            session = DBSession()
            print('数据库连接成功')
            return session
