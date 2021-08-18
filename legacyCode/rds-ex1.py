# Working with Amazon Aurora through Python... hopefully can take advantage of SQL functionality + Pandas for data analysis

import boto3
import pandas as pd
import pymysql

host = 'sampledb1-instance-1.codmbuo0zo1d.us-east-1.rds.amazonaws.com'
port = 3306
dbname = 'sampledb1-instance-1'
user = 'admin'
password = 'password'

#conn = pymysql.connect(host = host, user = user, port = port, passwd = password, db = dbname)\
conn = pymysql.connect(host = host, user = user, passwd = password)
print('Able to connect?', conn)

cursor = db.cursor()
cursor.execute('select version()')
