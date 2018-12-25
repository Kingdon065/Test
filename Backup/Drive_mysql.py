#!/usr/bin/python3

import pymysql
import os
from multiprocessing.pool import Pool
from functools import partial

drive = 'E:/'
file_type = ('FILE', 'DIR')


def size_format(size):
    if size >= 1024.0**3:
        size = size / (1024.0**3)
        size_info = (size, 'GB')
        return size_info
    elif size >= 1024.0**2:
        size = size / (1024.0**2)
        size_info = (size, 'MB')
        return size_info
    elif size >= 1024.0:
        size = size / 1024.0
        size_info = (size, 'KB')
        return size_info
    else:
        size_info = (size, 'B')
        return size_info


class MysqlOperator:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='mat', password='1980mk**', port=3306)
        self.db.set_charset('utf8mb4')
        self.cursor = self.db.cursor()
        sql = 'CREATE DATABASE IF NOT EXISTS drive'
        self.cursor.execute(sql)
        sql = 'USE drive'
        self.cursor.execute(sql)
        sql = 'CREATE TABLE IF NOT EXISTS \
                  drive_e (Filename varchar(256), Type VARCHAR(5), Size FLOAT(6,2), Unit varchar(3), Path VARCHAR(500))'
        self.cursor.execute(sql)
        self.data = {
            'Filename': '',
            'Type': '',
            'Size': 0,
            'Unit': '',
            'Path': ''
        }
        table = 'drive_e'
        keys = ', '.join(self.data.keys())
        values = ', '.join(['%s'] * len(self.data))
        self.sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)

    def reset_data(self):
        self.data['Size'] = 0
        self.data['Unit'] = ''

    def insert_data(self):
        try:
            self.cursor.execute(self.sql, tuple(self.data.values()))
            self.db.commit()
            print(self.data)
        except:
            self.db.rollback()


def save_to_mysql(path):
    mo = MysqlOperator()
    for folder, sub_folders, filenames in os.walk(path):
        folder = os.path.abspath(folder)
        for sub_folder in sub_folders:
            mo.data['Filename'] = sub_folder
            mo.data['Type'] = file_type[1]
            mo.data['Path'] = folder
            mo.insert_data()
        for filename in filenames:
            mo.data['Filename'] = filename
            mo.data['Type'] = file_type[0]
            mo.data['Path'] = folder
            try:
                size = os.path.getsize(os.path.join(folder, filename))
                size_info = size_format(size)
                mo.data['Size'] = size_info[0]
                mo.data['Unit'] = size_info[1]
                mo.insert_data()
            except:
                mo.reset_data()
                mo.insert_data()
        # 初始化Size和Unit
        mo.reset_data()


def list_root():
    mo = MysqlOperator()
    groups = []
    for filename in os.listdir(drive):
        fullpath = os.path.join(drive, filename)
        if os.path.isdir(fullpath):
            groups.append(fullpath)
        else:
            mo.data['Filename'] = filename
            mo.data['Type'] = file_type[0]
            mo.data['Path'] = fullpath
            try:
                size = os.path.getsize(fullpath)
                size_info = size_format(size)
                mo.data['Size'] = size_info[0]
                mo.data['Unit'] = size_info[1]
                mo.insert_data()
            except:
                mo.reset_data()
                mo.insert_data()
    mo.reset_data()
    return groups


def run():
    groups = list_root()
    pool = Pool()
    pool.map(save_to_mysql, groups)
    pool.close()
    pool.join()

if __name__ == '__main__':
    run()
