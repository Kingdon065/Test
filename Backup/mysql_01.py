#! python3

import pymysql
import csv


db = pymysql.connect(host='localhost', user='mat', password='1980mk**', port=3306, db='spiders')
db.set_charset('utf8mb4')
cursor = db.cursor()
#sql = 'CREATE TABLE IF NOT EXISTS
# maoyan (排名 INT(4), 片名 VARCHAR(100), 演员 VARCHAR(255), 上映时间 VARCHAR(100), 评分 FLOAT(1,1))'
#cursor.execute(sql)

sql = 'ALTER TABLE maoyan DROP 排名'
cursor.execute(sql)
sql = 'ALTER TABLE maoyan ADD 排名 INT(4) PRIMARY KEY AUTO_INCREMENT FIRST'
cursor.execute(sql)

csvfile = open('data.csv', 'r')
reader = csv.reader(csvfile)

for row in reader:
    if row[0] == '排名':
        continue
    data = {
        '排名': int(row[0]),
        '片名': row[1],
        '演员': row[2],
        '上映时间': row[3],
        '评分': float(row[4])
    }
    table = 'maoyan'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=table, keys=keys, values=values)
    update = ', '.join(['{key}=%s'.format(key=key) for key in data.keys()])
    sql += update
    try:
        cursor.execute(sql, tuple(data.values())*2)
        db.commit()
    except Exception as exc:
        print(exc)
        db.rollback()

sql = 'SELECT * FROM maoyan'
#sql2 = 'SELECT * FROM maoyan WHERE 排名 <= 10'
try:
    cursor.execute(sql)
    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()
except:
    print('error')
db.close()
